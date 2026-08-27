from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

from .models import Complaint, ComplaintStatus, ComplaintPriority
from accounts.models import User, StaffProfile, Role
from accounts.notifications import send_notification

logger = logging.getLogger(__name__)

@shared_task
def check_sla_violations():
    """
    Background job to monitor complaint ages against their Priority SLA limits.
    High/Critical: 24h, Medium: 72h, Low: 168h
    If violated:
    - Escalate status.
    - Notify Department Manager and System Admins.
    """
    logger.info("Starting SLA violation check...")
    
    # Active states
    active_statuses = [
        ComplaintStatus.SUBMITTED,
        ComplaintStatus.ACKNOWLEDGED,
        ComplaintStatus.ASSIGNED,
        ComplaintStatus.IN_PROGRESS,
        ComplaintStatus.ON_HOLD
    ]
    
    active_complaints = Complaint.objects.filter(status__in=active_statuses)
    now = timezone.now()
    escalated_count = 0

    # Get admin users for escalation notices
    admins = User.objects.filter(is_superuser=True) # Assuming superusers are Admins

    for complaint in active_complaints:
        age_hours = (now - complaint.created_at).total_seconds() / 3600
        
        sla_limit = None
        if complaint.priority in [ComplaintPriority.CRITICAL, ComplaintPriority.HIGH]:
            sla_limit = 24
        elif complaint.priority == ComplaintPriority.MEDIUM:
            sla_limit = 72
        elif complaint.priority == ComplaintPriority.LOW:
            sla_limit = 168
            
        if sla_limit and age_hours > sla_limit:
            # Escalation triggered
            complaint.status = ComplaintStatus.ESCALATED
            complaint.save()
            escalated_count += 1
            
            msg_title = "Complaint SLA Exceeded & Escalated"
            msg_body = f"Complaint {complaint.id} ({complaint.title}) has exceeded its {sla_limit}h SLA. Action required immediately."
            
            # Notify Department Manager
            if complaint.category and complaint.category.department:
                manager = complaint.category.department.manager
                if manager and manager.user:
                    send_notification(manager.user.id, msg_title, msg_body, reference_id=str(complaint.id))
            
            # Notify System Admins
            for admin in admins:
                send_notification(admin.id, msg_title, msg_body, reference_id=str(complaint.id))

    logger.info(f"SLA check completed. {escalated_count} complaints escalated.")
    return f"Escalated {escalated_count} complaints"
