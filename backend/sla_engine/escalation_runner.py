import logging
from django.utils import timezone
from django.db import transaction
from complaints.models import Complaint
from .models import SLAPolicy, EscalationTier, SLABreachRecord
from notifications.dispatcher import NotificationDispatcher

logger = logging.getLogger(__name__)

class EscalationRunner:
    """Automated SLA escalation processor running continuous checks and multi-tier alerting."""
    
    @classmethod
    @transaction.atomic
    def process_escalations(cls):
        now = timezone.now()
        breached_complaints = Complaint.objects.filter(
            status__in=["submitted", "triaged", "assigned", "in_progress"],
            sla_resolution_due__lt=now,
            is_sla_breached=False
        ).select_related("tenant", "department", "category", "assigned_worker")
        
        escalated_count = 0
        for c in breached_complaints:
            c.is_sla_breached = True
            c.sla_breach_level = 1
            c.status = "escalated"
            c.save(update_fields=["is_sla_breached", "sla_breach_level", "status"])
            
            delay = (now - c.sla_resolution_due).total_seconds() / 3600.0
            
            # Record breach audit log
            SLABreachRecord.objects.create(
                complaint_id=c.id,
                tracking_number=c.tracking_number,
                tier_reached=1,
                breached_at=now,
                delay_hours=round(delay, 2),
                root_cause="Automated SLA expiration trigger"
            )
            
            # Dispatch urgent escalation alerts to department head
            if c.department and c.department.head_of_department:
                NotificationDispatcher.send_notification(
                    recipient=c.department.head_of_department,
                    event_code="SLA_BREACH_TIER_1",
                    context={
                        "tracking_number": c.tracking_number,
                        "title": c.title,
                        "department": c.department.name,
                        "delay_hours": f"{delay:.1f}"
                    },
                    channels=["in_app", "email", "sms"]
                )
            escalated_count += 1
            
        logger.info(f"EscalationRunner processed {escalated_count} breached complaints.")
        return escalated_count
