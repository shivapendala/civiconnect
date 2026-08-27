import logging
from typing import Optional, List, Dict
from django.utils import timezone
from .models import Complaint, StatusTransitionLog

logger = logging.getLogger(__name__)

class ComplaintWorkflowEngine:
    """State machine rules, validation guards, and automated transitions for citizen grievances."""
    TRANSITION_MATRIX = {
        "submitted": ["triaged", "rejected", "duplicate"],
        "triaged": ["assigned", "rejected", "duplicate"],
        "assigned": ["in_progress", "triaged", "rejected"],
        "in_progress": ["resolved", "blocked", "escalated"],
        "blocked": ["in_progress", "assigned"],
        "resolved": ["verified", "in_progress", "escalated"],
        "verified": [],
        "rejected": ["submitted"],
        "duplicate": ["submitted"],
        "escalated": ["assigned", "in_progress", "resolved"]
    }

    @classmethod
    def is_transition_allowed(cls, from_status: str, to_status: str) -> bool:
        allowed = cls.TRANSITION_MATRIX.get(from_status, [])
        return to_status in allowed

    @classmethod
    def execute_transition(cls, complaint: Complaint, to_status: str, actor, reason: str = "") -> Complaint:
        from_status = complaint.status
        if not cls.is_transition_allowed(from_status, to_status):
            raise ValueError(f"Illegal status transition from {from_status} to {to_status}")
            
        complaint.status = to_status
        complaint.save()
        
        StatusTransitionLog.objects.create(
            complaint=complaint,
            actor=actor,
            from_status=from_status,
            to_status=to_status,
            reason=reason,
            timestamp=timezone.now()
        )
        logger.info(f"Transition executed: {complaint.tracking_number} [{from_status} -> {to_status}] by {actor}")
        return complaint
