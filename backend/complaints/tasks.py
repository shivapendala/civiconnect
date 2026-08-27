import logging
from celery import shared_task
from django.utils import timezone
from .models import Complaint
from .services import ComplaintService

logger = logging.getLogger(__name__)

@shared_task(name="complaints.auto_triage_pending_complaints")
def auto_triage_pending_complaints():
    """Scans submitted complaints and runs automated AI categorization and duplicate detection."""
    pending = Complaint.objects.filter(status="submitted").select_related("category", "tenant")
    triaged_count = 0
    
    for c in pending:
        try:
            from ai_routing.client import AIRoutingClient
            triage_res = AIRoutingClient.triage_description(c.description)
            if triage_res.get("suggested_priority"):
                c.priority = triage_res["suggested_priority"]
                c.ai_confidence_score = float(triage_res.get("confidence", 0.85))
                c.ai_predicted_category = triage_res.get("suggested_category", "")
                c.status = "triaged"
                c.save()
                triaged_count += 1
        except Exception as e:
            logger.error(f"Auto triage failed for {c.tracking_number}: {e}")
            
    logger.info(f"Auto-triaged {triaged_count} complaints.")
    return triaged_count

@shared_task(name="complaints.scan_sla_breaches")
def scan_sla_breaches():
    """Background task evaluating impending and breached SLAs."""
    from sla_engine.calculator import SLACalculator
    results = SLACalculator.evaluate_breaches()
    logger.info(f"SLA breach scan completed: {results}")
    return results
