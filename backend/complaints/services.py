import math
from django.db.models import Count, Q
from .models import Complaint, ComplaintAssignment, ComplaintStatus
from accounts.models import StaffProfile

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers.
    return c * r

def assign_complaint(complaint_id):
    """
    Smart Assignment Engine:
    1. Determine Department from Complaint Category.
    2. Find Available Staff in that Department.
    3. Sort by Lowest Workload (Active complaints).
    4. (Optional) Sort by Nearest Staff (if staff location is known).
    """
    try:
        complaint = Complaint.objects.get(id=complaint_id)
    except Complaint.DoesNotExist:
        return None, "Complaint not found"

    if not complaint.category or not complaint.category.department:
        return None, "Complaint category or department is missing"

    department = complaint.category.department

    # Get active statuses that represent 'workload'
    active_statuses = [
        ComplaintStatus.ASSIGNED, 
        ComplaintStatus.IN_PROGRESS, 
        ComplaintStatus.ON_HOLD
    ]

    # Query staff in this department, annotate with their current active workload
    # We count assignments where the related complaint is in an active status.
    staff_query = StaffProfile.objects.filter(
        department=department,
        user__is_active=True
    )
    
    # Isolate by municipality if complaint belongs to one
    if complaint.municipality:
        staff_query = staff_query.filter(municipality=complaint.municipality)
        
    staff_members = staff_query.annotate(
        active_workload=Count(
            'complaintassignment', 
            filter=Q(complaintassignment__complaint__status__in=active_statuses)
        )
    ).order_by('active_workload')

    if not staff_members.exists():
        # Fallback to assigning to the department without specific staff
        assignment = ComplaintAssignment.objects.create(
            complaint=complaint,
            department=department,
            staff=None
        )
        complaint.status = ComplaintStatus.ACKNOWLEDGED
        complaint.save()
        return assignment, "Assigned to department queue (No available staff)"

    # Here we would factor in distance if staff locations were tracked in real-time.
    # For now, we take the staff with the lowest workload (first in ordered queryset).
    best_staff = staff_members.first()

    # Create the assignment
    assignment = ComplaintAssignment.objects.create(
        complaint=complaint,
        department=department,
        staff=best_staff
    )

    # Update complaint status
    complaint.status = ComplaintStatus.ASSIGNED
    complaint.save()

    return assignment, f"Assigned to {best_staff.user.email} (Workload: {best_staff.active_workload})"

def override_assignment(complaint_id, new_staff_profile_id):
    """
    Manual Override: Allows Admin to reassign a complaint to a specific staff member.
    """
    try:
        complaint = Complaint.objects.get(id=complaint_id)
        new_staff = StaffProfile.objects.get(id=new_staff_profile_id)
    except (Complaint.DoesNotExist, StaffProfile.DoesNotExist):
        return False, "Complaint or Staff not found"

    # We can either update the existing assignment or create a new one to keep history.
    # Creating a new one is often better for audit trails.
    assignment = ComplaintAssignment.objects.create(
        complaint=complaint,
        department=new_staff.department,
        staff=new_staff
    )

    if complaint.status == ComplaintStatus.ACKNOWLEDGED or complaint.status == ComplaintStatus.SUBMITTED:
        complaint.status = ComplaintStatus.ASSIGNED
        complaint.save()

    return True, f"Manually reassigned to {new_staff.user.email}"

from .models import Resolution, ResolutionEvidence, Feedback
from accounts.notifications import send_notification

def resolve_complaint(complaint_id, staff_profile_id, summary, file_url=""):
    """
    Called by Staff to mark a complaint as RESOLVED.
    """
    try:
        complaint = Complaint.objects.get(id=complaint_id)
        staff = StaffProfile.objects.get(id=staff_profile_id)
    except (Complaint.DoesNotExist, StaffProfile.DoesNotExist):
        return False, "Complaint or Staff not found"

    # Create Resolution record
    resolution, created = Resolution.objects.get_or_create(
        complaint=complaint,
        defaults={'staff': staff, 'summary': summary}
    )
    if not created:
        resolution.summary = summary
        resolution.save()

    if file_url:
        ResolutionEvidence.objects.create(resolution=resolution, file_url=file_url)

    complaint.status = ComplaintStatus.RESOLVED
    complaint.save()

    # Notify Citizen
    send_notification(
        complaint.citizen.user.id,
        "Complaint Resolved",
        f"Your complaint {complaint.id} has been marked as resolved. Please verify.",
        reference_id=str(complaint.id)
    )

    return True, "Complaint resolved successfully"

def verify_complaint(complaint_id, citizen_id, rating, comments=""):
    """
    Called by Citizen to accept the resolution and close the workflow.
    """
    try:
        complaint = Complaint.objects.get(id=complaint_id, citizen_id=citizen_id)
    except Complaint.DoesNotExist:
        return False, "Complaint not found or unauthorized"

    if complaint.status != ComplaintStatus.RESOLVED:
        return False, "Complaint must be resolved before verification"

    complaint.status = ComplaintStatus.CITIZEN_VERIFIED
    complaint.save()

    Feedback.objects.create(
        complaint=complaint,
        citizen=complaint.citizen,
        rating=rating,
        comments=comments
    )
    
    # After verification, the system officially CLOSES it.
    complaint.status = ComplaintStatus.CLOSED
    complaint.save()

    return True, "Complaint verified and closed"

def reopen_complaint(complaint_id, citizen_id, reason):
    """
    Called by Citizen to reject the resolution and reopen the workflow.
    """
    try:
        complaint = Complaint.objects.get(id=complaint_id, citizen_id=citizen_id)
    except Complaint.DoesNotExist:
        return False, "Complaint not found or unauthorized"

    complaint.status = ComplaintStatus.REOPENED
    complaint.save()

    # Notify Staff/Department
    assignment = getattr(complaint, 'complaintassignment_set', None)
    if assignment and assignment.exists():
        last_assignment = assignment.last()
        if last_assignment.staff:
            send_notification(
                last_assignment.staff.user.id,
                "Complaint Reopened",
                f"Complaint {complaint.id} was reopened by the citizen. Reason: {reason}",
                reference_id=str(complaint.id)
            )

    return True, "Complaint reopened"
