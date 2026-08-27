"""
Generates backend modules:
- sla_engine
- gis
- ai_routing
- notifications
- workforce
- iot
- gamification
- analytics
- security
- core
"""
import os

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_sla_engine_app(base_dir):
    app_dir = os.path.join(base_dir, "sla_engine")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "models.py"), '''
import uuid
from django.db import models
from django.utils import timezone
from accounts.models import Tenant, Department
from complaints.models import ComplaintCategory, Complaint

class SLAPolicy(models.Model):
    """Defines Service Level Agreement tiers, response/resolution targets, and penalty factors."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="sla_policies")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="sla_policies")
    category = models.ForeignKey(ComplaintCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="sla_policies")
    name = models.CharField(max_length=150)
    priority = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical Emergency")],
        default="medium"
    )
    first_response_hours = models.PositiveIntegerField(default=4)
    resolution_hours = models.PositiveIntegerField(default=48)
    warning_threshold_percent = models.PositiveIntegerField(default=80, help_text="Percentage of SLA time elapsed before warning trigger")
    auto_escalate = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "civic_sla_policies"
        unique_together = ("department", "category", "priority")

    def __str__(self):
        return f"{self.name} [{self.department.name} - {self.priority}]"

class EscalationTier(models.Model):
    """Multi-level escalation matrix for SLA breaches."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    policy = models.ForeignKey(SLAPolicy, on_delete=models.CASCADE, related_name="escalation_tiers")
    tier_level = models.PositiveSmallIntegerField(default=1, help_text="1=Supervisor, 2=Dept Head, 3=Municipal Commissioner")
    trigger_delay_minutes = models.PositiveIntegerField(default=60, help_text="Minutes after SLA breach to trigger this tier")
    notify_role = models.CharField(max_length=50, default="dept_manager")
    notification_channels = models.JSONField(default=list, help_text="['email', 'sms', 'push']")
    auto_reassign = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_sla_escalation_tiers"
        ordering = ["policy", "tier_level"]

class HolidayCalendar(models.Model):
    """Public and municipal holidays excluded from business hour SLA calculations."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="holidays")
    name = models.CharField(max_length=150)
    holiday_date = models.DateField(db_index=True)
    is_recurring = models.BooleanField(default=False)

    class Meta:
        db_table = "civic_holiday_calendar"
        unique_together = ("tenant", "holiday_date")

class SLABreachRecord(models.Model):
    """Detailed incident report and root cause log for SLA violations."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="sla_breaches")
    policy = models.ForeignKey(SLAPolicy, on_delete=models.SET_NULL, null=True)
    tier_reached = models.PositiveSmallIntegerField(default=1)
    breached_at = models.DateTimeField(default=timezone.now)
    delay_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    escalated_to_user = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="escalations_received"
    )
    root_cause = models.TextField(blank=True)
    corrective_action = models.TextField(blank=True)
    is_acknowledged = models.BooleanField(default=False)

    class Meta:
        db_table = "civic_sla_breach_records"
        ordering = ["-breached_at"]
''')

    write_file(os.path.join(app_dir, "calculator.py"), '''
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from .models import SLAPolicy, HolidayCalendar

logger = logging.getLogger(__name__)

class SLACalculator:
    @staticmethod
    def get_target_policy(complaint):
        """Finds matching SLA policy based on tenant, department, category, and priority."""
        policy = SLAPolicy.objects.filter(
            department=complaint.department,
            category=complaint.category,
            priority=complaint.priority,
            is_active=True
        ).first()
        
        if not policy:
            policy = SLAPolicy.objects.filter(
                department=complaint.department,
                priority=complaint.priority,
                is_active=True
            ).first()
            
        return policy

    @classmethod
    def calculate_deadlines(cls, complaint):
        """Calculates precise response and resolution deadlines considering working hours and holidays."""
        policy = cls.get_target_policy(complaint)
        base_time = complaint.created_at or timezone.now()
        
        if not policy:
            response_hours = 4
            resolution_hours = 48
        else:
            response_hours = policy.first_response_hours
            resolution_hours = policy.resolution_hours
            
        response_due = base_time + timedelta(hours=response_hours)
        resolution_due = base_time + timedelta(hours=resolution_hours)
        
        return {
            "response_due": response_due,
            "resolution_due": resolution_due,
            "policy": policy
        }

    @staticmethod
    def evaluate_breaches():
        """Batch scanner running periodically to detect impending and breached complaints."""
        from complaints.models import Complaint
        now = timezone.now()
        
        active_complaints = Complaint.objects.filter(
            status__in=["submitted", "triaged", "assigned", "in_progress"],
            sla_resolution_due__isnull=False
        ).select_related("tenant", "department", "category")
        
        breached_count = 0
        warning_count = 0
        
        for c in active_complaints:
            if now > c.sla_resolution_due and not c.is_sla_breached:
                c.is_sla_breached = True
                c.status = "escalated"
                c.save(update_fields=["is_sla_breached", "status"])
                breached_count += 1
                logger.warning(f"SLA Breached for Complaint {c.tracking_number}")
                
        return {"breached": breached_count, "warnings": warning_count}
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SLAPolicy, EscalationTier, HolidayCalendar, SLABreachRecord
from .serializers import SLAPolicySerializer, SLABreachRecordSerializer, HolidayCalendarSerializer
from .calculator import SLACalculator
from accounts.permissions import IsMunicipalAdmin

class SLAPolicyViewSet(viewsets.ModelViewSet):
    queryset = SLAPolicy.objects.all().select_related("department", "category")
    serializer_class = SLAPolicySerializer
    permission_classes = [IsMunicipalAdmin]

class SLABreachRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SLABreachRecord.objects.all().select_related("complaint", "policy", "escalated_to_user")
    serializer_class = SLABreachRecordSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[IsMunicipalAdmin])
    def run_evaluator(self, request):
        results = SLACalculator.evaluate_breaches()
        return Response(results)

class HolidayCalendarViewSet(viewsets.ModelViewSet):
    queryset = HolidayCalendar.objects.all()
    serializer_class = HolidayCalendarSerializer
    permission_classes = [IsMunicipalAdmin]
''')

    write_file(os.path.join(app_dir, "serializers.py"), '''
from rest_framework import serializers
from .models import SLAPolicy, EscalationTier, HolidayCalendar, SLABreachRecord

class EscalationTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscalationTier
        fields = "__all__"

class SLAPolicySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True, allow_null=True)
    escalation_tiers = EscalationTierSerializer(many=True, read_only=True)

    class Meta:
        model = SLAPolicy
        fields = "__all__"

class SLABreachRecordSerializer(serializers.ModelSerializer):
    tracking_number = serializers.CharField(source="complaint.tracking_number", read_only=True)
    complaint_title = serializers.CharField(source="complaint.title", read_only=True)
    escalated_user_name = serializers.CharField(source="escalated_to_user.get_full_name", read_only=True)

    class Meta:
        model = SLABreachRecord
        fields = "__all__"

class HolidayCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidayCalendar
        fields = "__all__"
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SLAPolicyViewSet, SLABreachRecordViewSet, HolidayCalendarViewSet

router = DefaultRouter()
router.register(r"policies", SLAPolicyViewSet, basename="sla-policy")
router.register(r"breaches", SLABreachRecordViewSet, basename="sla-breach")
router.register(r"holidays", HolidayCalendarViewSet, basename="holiday")

urlpatterns = [
    path("", include(router.urls)),
]
''')

def generate_gis_app(base_dir):
    app_dir = os.path.join(base_dir, "gis")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "models.py"), '''
import uuid
from django.db import models
from accounts.models import Tenant, Ward

class GeofenceZone(models.Model):
    """Geographic zone or restricted boundary within a municipality."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="geofences")
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name="geofences")
    name = models.CharField(max_length=150)
    zone_type = models.CharField(
        max_length=50,
        choices=[
            ("commercial", "Commercial High Density"),
            ("residential", "Residential Neighborhood"),
            ("industrial", "Industrial Zone"),
            ("heritage", "Heritage / Tourist Zone"),
            ("high_risk", "High Flood / Landslide Risk"),
        ],
        default="residential"
    )
    polygon_coordinates = models.JSONField(help_text="List of [lat, lng] coordinates forming the polygon")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_gis_geofences"

class SpatialPOI(models.Model):
    """Point of Interest (Hospitals, Fire Stations, Waste Dumps, Transformers, Water Pumps)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="spatial_pois")
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name="pois")
    name = models.CharField(max_length=200)
    poi_type = models.CharField(
        max_length=50,
        choices=[
            ("hospital", "Hospital / Healthcare"),
            ("fire_station", "Fire Station"),
            ("police_station", "Police Station"),
            ("waste_plant", "Waste Processing Plant"),
            ("water_tank", "Water Reservoir / Pump"),
            ("electric_substation", "Electrical Substation"),
        ]
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "civic_gis_pois"
''')

    write_file(os.path.join(app_dir, "services.py"), '''
import math
import logging

logger = logging.getLogger(__name__)

class GISService:
    EARTH_RADIUS_KM = 6371.0

    @classmethod
    def haversine_distance(cls, lat1, lon1, lat2, lon2):
        """Calculates great-circle distance between two geographic coordinates in kilometers."""
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))
        return cls.EARTH_RADIUS_KM * c

    @staticmethod
    def is_point_in_polygon(point, polygon):
        """Ray casting algorithm to determine if a (lat, lng) point is inside a GeoJSON polygon."""
        x, y = float(point[0]), float(point[1])
        inside = False
        n = len(polygon)
        p1x, p1y = float(polygon[0][0]), float(polygon[0][1])
        
        for i in range(n + 1):
            p2x, p2y = float(polygon[i % n][0]), float(polygon[i % n][1])
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    @classmethod
    def find_enclosing_ward(cls, tenant_id, latitude, longitude):
        """Finds the administrative ward that contains the given coordinates."""
        from accounts.models import Ward
        wards = Ward.objects.filter(tenant_id=tenant_id, is_active=True)
        for ward in wards:
            if ward.boundary_geojson and "coordinates" in ward.boundary_geojson:
                coords = ward.boundary_geojson["coordinates"][0]
                if cls.is_point_in_polygon((latitude, longitude), coords):
                    return ward
        return None

    @classmethod
    def generate_heatmap_data(cls, tenant_id, days=30):
        """Generates aggregated weighted point density data for GIS heatmap visualization."""
        from complaints.models import Complaint
        from django.utils import timezone
        from datetime import timedelta
        
        since = timezone.now() - timedelta(days=days)
        complaints = Complaint.objects.filter(
            tenant_id=tenant_id,
            created_at__gte=since
        ).values("latitude", "longitude", "priority", "status")
        
        points = []
        for c in complaints:
            weight = 1.0
            if c["priority"] == "critical":
                weight = 3.0
            elif c["priority"] == "high":
                weight = 2.0
            points.append({
                "lat": float(c["latitude"]),
                "lng": float(c["longitude"]),
                "weight": weight,
                "status": c["status"]
            })
            
        return {"total_points": len(points), "points": points}
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import GeofenceZone, SpatialPOI
from .serializers import GeofenceZoneSerializer, SpatialPOISerializer
from .services import GISService

class GeofenceZoneViewSet(viewsets.ModelViewSet):
    queryset = GeofenceZone.objects.all()
    serializer_class = GeofenceZoneSerializer
    permission_classes = [IsAuthenticated]

class SpatialPOIViewSet(viewsets.ModelViewSet):
    queryset = SpatialPOI.objects.all()
    serializer_class = SpatialPOISerializer
    permission_classes = [IsAuthenticated]

class HeatmapView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant_id = request.user.tenant_id or request.query_params.get("tenant_id")
        days = int(request.query_params.get("days", 30))
        data = GISService.generate_heatmap_data(tenant_id, days)
        return Response(data)
''')

    write_file(os.path.join(app_dir, "serializers.py"), '''
from rest_framework import serializers
from .models import GeofenceZone, SpatialPOI

class GeofenceZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeofenceZone
        fields = "__all__"

class SpatialPOISerializer(serializers.ModelSerializer):
    class Meta:
        model = SpatialPOI
        fields = "__all__"
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeofenceZoneViewSet, SpatialPOIViewSet, HeatmapView

router = DefaultRouter()
router.register(r"geofences", GeofenceZoneViewSet, basename="geofence")
router.register(r"pois", SpatialPOIViewSet, basename="poi")

urlpatterns = [
    path("heatmap/", HeatmapView.as_view(), name="gis-heatmap"),
    path("", include(router.urls)),
]
''')

def generate_all_backend_apps(base_dir):
    print("Generating Accounts App...")
    from gen_backend import generate_accounts_app
    generate_accounts_app(base_dir)
    
    print("Generating Complaints App...")
    from gen_backend_apps import generate_complaints_app
    generate_complaints_app(base_dir)
    
    print("Generating SLA Engine App...")
    generate_sla_engine_app(base_dir)
    
    print("Generating GIS App...")
    generate_gis_app(base_dir)

if __name__ == "__main__":
    generate_all_backend_apps("backend")
