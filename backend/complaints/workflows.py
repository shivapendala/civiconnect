import logging
from accounts.models import Department
from complaints.models import Complaint, ComplaintStatus

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """State machine rules and routing engine for citizen grievances."""

    TRANSITION_MATRIX = {
        ComplaintStatus.SUBMITTED: [ComplaintStatus.ACKNOWLEDGED, ComplaintStatus.ASSIGNED, ComplaintStatus.REJECTED],
        ComplaintStatus.ACKNOWLEDGED: [ComplaintStatus.ASSIGNED, ComplaintStatus.IN_PROGRESS, ComplaintStatus.REJECTED],
        ComplaintStatus.ASSIGNED: [ComplaintStatus.IN_PROGRESS, ComplaintStatus.ON_HOLD, ComplaintStatus.REJECTED],
        ComplaintStatus.IN_PROGRESS: [ComplaintStatus.RESOLVED, ComplaintStatus.ON_HOLD, ComplaintStatus.ESCALATED],
        ComplaintStatus.ON_HOLD: [ComplaintStatus.IN_PROGRESS, ComplaintStatus.ASSIGNED],
        ComplaintStatus.RESOLVED: [ComplaintStatus.CITIZEN_VERIFIED, ComplaintStatus.REOPENED, ComplaintStatus.CLOSED],
        ComplaintStatus.CITIZEN_VERIFIED: [ComplaintStatus.CLOSED, ComplaintStatus.REOPENED],
        ComplaintStatus.REOPENED: [ComplaintStatus.IN_PROGRESS, ComplaintStatus.ASSIGNED],
        ComplaintStatus.ESCALATED: [ComplaintStatus.IN_PROGRESS, ComplaintStatus.ASSIGNED, ComplaintStatus.RESOLVED],
        ComplaintStatus.REJECTED: [ComplaintStatus.SUBMITTED],
        ComplaintStatus.CLOSED: [],
    }

    @classmethod
    def evaluate_routing(cls, complaint: Complaint) -> Department:
        """Determines target department based on priority and category."""
        muni = complaint.municipality
        title_desc = f"{complaint.title} {complaint.description}".lower()
        cat_name = complaint.category.name.lower() if complaint.category else ""

        if ("pothole" in title_desc or "pothole" in cat_name) and complaint.priority == "CRITICAL":
            dept = Department.objects.filter(municipality=muni, name__icontains="Emergency").first()
            if dept:
                return dept

        if "water" in cat_name or "water" in title_desc:
            dept = Department.objects.filter(municipality=muni, name__icontains="Water").first()
            if dept:
                return dept

        # Fallback to General Services
        dept = Department.objects.filter(municipality=muni, name__icontains="General").first()
        if dept:
            return dept
            
        return Department.objects.filter(municipality=muni).first()

    @classmethod
    def process_state_transition(cls, complaint: Complaint, new_status: str):
        """Transitions complaint status if valid."""
        allowed = cls.TRANSITION_MATRIX.get(complaint.status, [])
        if new_status not in allowed:
            return False, f"Invalid transition from {complaint.status} to {new_status}"
            
        complaint.status = new_status
        complaint.save()
        return True, "Transition successful"

# Alias for backwards compatibility
ComplaintWorkflowEngine = WorkflowEngine
