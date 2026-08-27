from .models import Complaint, ComplaintStatus, SLARule
from accounts.models import Department
import json

class WorkflowEngine:
    """
    Business Process Model and Notation (BPMN) / Workflow Engine Mock.
    In a real massive app, this would use Camunda or a dedicated rules engine.
    Here we evaluate simple JSON-based decision trees for complaint routing.
    """
    
    @classmethod
    def evaluate_routing(cls, complaint: Complaint):
        """
        Dynamically route the complaint to the correct department based on
        its category, priority, and text content.
        """
        if not complaint.category:
            return None
            
        # Example Workflow Logic rules (normally stored in DB for dynamic admin configuration)
        # e.g., if Category=Pothole and Priority=Critical, send to Emergency Public Works
        routing_rules = [
            {
                "conditions": {"category_name": "Pothole", "priority": "CRITICAL"},
                "action": {"assign_department": "Emergency Public Works"}
            },
            {
                "conditions": {"category_name": "Water Leak"},
                "action": {"assign_department": "Water Services"}
            }
        ]
        
        assigned_dept_name = None
        for rule in routing_rules:
            conditions = rule.get("conditions", {})
            match = True
            if "category_name" in conditions and complaint.category.name != conditions["category_name"]:
                match = False
            if "priority" in conditions and complaint.priority != conditions["priority"]:
                match = False
                
            if match:
                assigned_dept_name = rule["action"].get("assign_department")
                break
                
        if assigned_dept_name:
            try:
                dept = Department.objects.get(name=assigned_dept_name, municipality=complaint.municipality)
                return dept
            except Department.DoesNotExist:
                return complaint.category.department
        
        return complaint.category.department

    @classmethod
    def process_state_transition(cls, complaint: Complaint, new_status: str, user=None):
        """
        Ensure state transitions follow allowed workflow paths.
        e.g., Cannot go from SUBMITTED to RESOLVED directly without IN_PROGRESS.
        """
        allowed_transitions = {
            ComplaintStatus.SUBMITTED: [ComplaintStatus.ACKNOWLEDGED, ComplaintStatus.REJECTED],
            ComplaintStatus.ACKNOWLEDGED: [ComplaintStatus.ASSIGNED],
            ComplaintStatus.ASSIGNED: [ComplaintStatus.IN_PROGRESS, ComplaintStatus.ON_HOLD],
            ComplaintStatus.IN_PROGRESS: [ComplaintStatus.RESOLVED, ComplaintStatus.ON_HOLD, ComplaintStatus.ESCALATED],
            ComplaintStatus.ON_HOLD: [ComplaintStatus.IN_PROGRESS],
            ComplaintStatus.RESOLVED: [ComplaintStatus.CITIZEN_VERIFIED, ComplaintStatus.REOPENED],
            ComplaintStatus.CITIZEN_VERIFIED: [ComplaintStatus.CLOSED],
            ComplaintStatus.REOPENED: [ComplaintStatus.IN_PROGRESS],
            ComplaintStatus.ESCALATED: [ComplaintStatus.IN_PROGRESS],
            ComplaintStatus.CLOSED: [],
            ComplaintStatus.REJECTED: [],
        }
        
        current_status = complaint.status
        valid_next_states = allowed_transitions.get(current_status, [])
        
        if new_status in valid_next_states:
            complaint.status = new_status
            complaint.save()
            return True, "Transition successful"
        else:
            return False, f"Invalid workflow transition from {current_status} to {new_status}"
