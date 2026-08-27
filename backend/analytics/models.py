import uuid
from django.db import models
from django.utils import timezone
from accounts.models import Tenant, Ward, Department

class DailyWardMetric(models.Model):
    """Aggregated daily operational metric snapshot per ward."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="ward_metrics")
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="daily_metrics")
    metric_date = models.DateField(db_index=True)
    
    complaints_logged = models.PositiveIntegerField(default=0)
    complaints_resolved = models.PositiveIntegerField(default=0)
    complaints_breached = models.PositiveIntegerField(default=0)
    avg_resolution_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    citizen_satisfaction_score = models.DecimalField(max_digits=4, decimal_places=2, default=4.5)
    active_field_workers = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_analytics_daily_ward_metrics"
        unique_together = ("ward", "metric_date")
        ordering = ["-metric_date"]

class ExecutiveKPI(models.Model):
    """Executive level KPI metrics for city mayor, council members, and commissioners."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="executive_kpis")
    snapshot_date = models.DateField(db_index=True)
    overall_sla_compliance = models.DecimalField(max_digits=5, decimal_places=2, default=95.0)
    first_response_compliance = models.DecimalField(max_digits=5, decimal_places=2, default=92.0)
    citizen_nps_score = models.IntegerField(default=65)
    pothole_resolution_avg_hours = models.DecimalField(max_digits=5, decimal_places=2, default=24.0)
    sanitation_resolution_avg_hours = models.DecimalField(max_digits=5, decimal_places=2, default=12.0)
    water_leak_resolution_avg_hours = models.DecimalField(max_digits=5, decimal_places=2, default=18.0)
    streetlight_uptime_percent = models.DecimalField(max_digits=5, decimal_places=2, default=99.2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_analytics_executive_kpis"
        unique_together = ("tenant", "snapshot_date")
