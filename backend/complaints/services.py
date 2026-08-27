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
    staff_members = StaffProfile.objects.filter(
        department=department,
        user__is_active=True
    ).annotate(
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
