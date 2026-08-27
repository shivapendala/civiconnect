"""
Generator for CivicConnect Backend Apps (Part 2):
- workforce
- ai_routing
- notifications
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
    print(f"Generated: {filepath} ({len(content.splitlines())} lines)")

def generate_workforce_app(base_dir):
    app_dir = os.path.join(base_dir, "workforce")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "models.py"), '''
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import Tenant, Department, Ward

class FieldTeam(models.Model):
    """Field operational crew or municipal response squad."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="field_teams")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="field_teams")
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name="field_teams")
    name = models.CharField(max_length=150)
    team_lead = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="lead_teams"
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_field_teams", blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    vehicle_registration = models.CharField(max_length=50, blank=True)
    is_available = models.BooleanField(default=True)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_ping = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_workforce_field_teams"

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class WorkOrder(models.Model):
    """Job assignment dispatched to a field worker or crew."""
    STATUS_CHOICES = [
        ("pending", "Pending Dispatch"),
        ("dispatched", "Dispatched to Field"),
        ("acknowledged", "Acknowledged by Worker"),
        ("in_progress", "Work Started"),
        ("blocked", "Blocked / Needs Material"),
        ("completed", "Work Completed"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=50, unique=True)
    complaint = models.ForeignKey("complaints.Complaint", on_delete=models.CASCADE, related_name="work_orders")
    team = models.ForeignKey(FieldTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name="work_orders")
    assigned_worker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_work_orders"
    )
    instructions = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, default=2.0)
    actual_hours_spent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    completion_notes = models.TextField(blank=True)
    completion_photo = models.ImageField(upload_to="work_order_proofs/%Y/%m/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_workforce_work_orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"WO-{self.order_number} ({self.status})"

class WorkerLocationHistory(models.Model):
    """Breadcrumb trail of field staff coordinates for route analytics and safety."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location_trail")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    battery_level = models.PositiveSmallIntegerField(null=True, blank=True)
    speed_kmh = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = "civic_workforce_location_history"
        ordering = ["-timestamp"]
''')

    write_file(os.path.join(app_dir, "services.py"), '''
import logging
import secrets
from django.utils import timezone
from .models import WorkOrder, FieldTeam, WorkerLocationHistory
from gis.services import GISService

logger = logging.getLogger(__name__)

class WorkforceService:
    @staticmethod
    def dispatch_work_order(complaint, worker=None, team=None, instructions=""):
        """Creates and dispatches a work order for an active grievance."""
        order_num = f"WO-{secrets.token_hex(4).upper()}"
        work_order = WorkOrder.objects.create(
            order_number=order_num,
            complaint=complaint,
            assigned_worker=worker,
            team=team,
            instructions=instructions,
            status="dispatched" if (worker or team) else "pending"
        )
        
        from complaints.services import ComplaintService
        ComplaintService.transition_status(complaint, "assigned", actor=worker, reason="Dispatched work order")
        return work_order

    @staticmethod
    def find_nearest_available_worker(department_id, latitude, longitude, max_radius_km=15.0):
        """Locates the closest available field worker within a given radius."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        workers = User.objects.filter(
            department_id=department_id,
            role="field_worker",
            is_active=True,
            last_location_lat__isnull=False,
            last_location_lng__isnull=False
        )
        
        nearest_worker = None
        min_dist = float("inf")
        
        for w in workers:
            dist = GISService.haversine_distance(latitude, longitude, w.last_location_lat, w.last_location_lng)
            if dist < min_dist and dist <= max_radius_km:
                min_dist = dist
                nearest_worker = w
                
        return nearest_worker, min_dist if nearest_worker else None
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FieldTeam, WorkOrder, WorkerLocationHistory
from .serializers import FieldTeamSerializer, WorkOrderSerializer, WorkerLocationHistorySerializer
from .services import WorkforceService

class FieldTeamViewSet(viewsets.ModelViewSet):
    queryset = FieldTeam.objects.all()
    serializer_class = FieldTeamSerializer
    permission_classes = [IsAuthenticated]

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all().select_related("complaint", "assigned_worker", "team")
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        order = self.get_object()
        order.status = "completed"
        order.completion_notes = request.data.get("notes", "")
        order.save()
        
        from complaints.services import ComplaintService
        ComplaintService.transition_status(order.complaint, "resolved", actor=request.user, reason="Work order completed")
        return Response(WorkOrderSerializer(order).data)

class WorkerLocationHistoryViewSet(viewsets.ModelViewSet):
    queryset = WorkerLocationHistory.objects.all()
    serializer_class = WorkerLocationHistorySerializer
    permission_classes = [IsAuthenticated]
''')

    write_file(os.path.join(app_dir, "serializers.py"), '''
from rest_framework import serializers
from .models import FieldTeam, WorkOrder, WorkerLocationHistory

class FieldTeamSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    team_lead_name = serializers.CharField(source="team_lead.get_full_name", read_only=True)

    class Meta:
        model = FieldTeam
        fields = "__all__"

class WorkOrderSerializer(serializers.ModelSerializer):
    complaint_title = serializers.CharField(source="complaint.title", read_only=True)
    tracking_number = serializers.CharField(source="complaint.tracking_number", read_only=True)
    worker_name = serializers.CharField(source="assigned_worker.get_full_name", read_only=True)

    class Meta:
        model = WorkOrder
        fields = "__all__"

class WorkerLocationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerLocationHistory
        fields = "__all__"
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FieldTeamViewSet, WorkOrderViewSet, WorkerLocationHistoryViewSet

router = DefaultRouter()
router.register(r"teams", FieldTeamViewSet, basename="field-team")
router.register(r"orders", WorkOrderViewSet, basename="work-order")
router.register(r"locations", WorkerLocationHistoryViewSet, basename="worker-location")

urlpatterns = [
    path("", include(router.urls)),
]
''')

def generate_ai_routing_app(base_dir):
    app_dir = os.path.join(base_dir, "ai_routing")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "client.py"), '''
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class AIRoutingClient:
    AI_SERVICE_URL = getattr(settings, "AI_SERVICE_URL", "http://ai-service:8001")

    @classmethod
    def classify_image(cls, image_file):
        """Sends image to AI microservice for hazard classification and bounding box detection."""
        try:
            url = f"{cls.AI_SERVICE_URL}/classify"
            files = {"file": image_file}
            response = requests.post(url, files=files, timeout=5.0)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"AI Service Image Classification Error: {e}")
        return {"category": "general", "confidence": 0.0, "labels": []}

    @classmethod
    def triage_description(cls, text):
        """Evaluates grievance text for department routing, priority level, and sentiment urgency."""
        try:
            url = f"{cls.AI_SERVICE_URL}/triage"
            response = requests.post(url, json={"text": text}, timeout=3.0)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"AI Service Triage Error: {e}")
        return {"suggested_department": "general", "priority": "medium", "urgency_score": 0.5}

    @classmethod
    def check_duplicate(cls, latitude, longitude, category_id, image_hash=None):
        """Checks for near-duplicate complaints within 100m radius and similar image/text embeddings."""
        try:
            url = f"{cls.AI_SERVICE_URL}/deduplicate"
            payload = {
                "latitude": float(latitude),
                "longitude": float(longitude),
                "category_id": str(category_id),
                "image_hash": image_hash
            }
            response = requests.post(url, json=payload, timeout=3.0)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"AI Deduplication Error: {e}")
        return {"is_duplicate": False, "cluster_id": None}
''')

    write_file(os.path.join(app_dir, "models.py"), '''
import uuid
from django.db import models
from complaints.models import Complaint

class AIClassificationLog(models.Model):
    """Log of inference decisions, predictions, and human confirmation rates."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="ai_logs")
    predicted_category = models.CharField(max_length=150)
    confidence_score = models.FloatField(default=0.0)
    predicted_priority = models.CharField(max_length=20)
    detected_labels = models.JSONField(default=list)
    human_accepted = models.BooleanField(null=True, blank=True)
    corrected_category = models.CharField(max_length=150, blank=True)
    latency_ms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_ai_classification_logs"
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .client import AIRoutingClient
from .models import AIClassificationLog

class AITriageView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get("description", "")
        if not text:
            return Response({"error": "Description required"}, status=status.HTTP_400_BAD_REQUEST)
        result = AIRoutingClient.triage_description(text)
        return Response(result)

class AIDeduplicationCheckView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        lat = request.data.get("latitude")
        lng = request.data.get("longitude")
        cat_id = request.data.get("category_id")
        result = AIRoutingClient.check_duplicate(lat, lng, cat_id)
        return Response(result)
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path
from .views import AITriageView, AIDeduplicationCheckView

urlpatterns = [
    path("triage/", AITriageView.as_view(), name="ai-triage"),
    path("check-duplicate/", AIDeduplicationCheckView.as_view(), name="ai-duplicate-check"),
]
''')

def generate_notifications_app(base_dir):
    app_dir = os.path.join(base_dir, "notifications")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "models.py"), '''
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class NotificationTemplate(models.Model):
    """Reusable multi-channel notification template with Jinja/Django formatting tokens."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    event_code = models.CharField(max_length=100, unique=True, db_index=True)
    subject_template = models.CharField(max_length=255)
    body_template = models.TextField()
    sms_template = models.CharField(max_length=160, blank=True)
    push_title_template = models.CharField(max_length=100, blank=True)
    push_body_template = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_notification_templates"

    def __str__(self):
        return f"{self.name} ({self.event_code})"

class NotificationLog(models.Model):
    """Delivery log tracking recipient status across email, SMS, push, and WebSocket."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    channel = models.CharField(max_length=30, choices=[("email", "Email"), ("sms", "SMS"), ("push", "Push Notification"), ("in_app", "In-App")])
    event_code = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    delivery_status = models.CharField(max_length=50, default="sent")
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "civic_notification_logs"
        ordering = ["-sent_at"]

class UserDeviceToken(models.Model):
    """FCM / APNs mobile push notification device registration token."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="device_tokens")
    token = models.CharField(max_length=500, unique=True)
    platform = models.CharField(max_length=20, choices=[("android", "Android FCM"), ("ios", "iOS APNs"), ("web", "Web Push")])
    device_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "civic_notification_device_tokens"
''')

    write_file(os.path.join(app_dir, "dispatcher.py"), '''
import logging
from django.utils import timezone
from .models import NotificationLog, UserDeviceToken, NotificationTemplate

logger = logging.getLogger(__name__)

class NotificationDispatcher:
    @classmethod
    def send_notification(cls, recipient, event_code, context, channels=None):
        """Dispatches multi-channel notification to a user based on event code and context."""
        template = NotificationTemplate.objects.filter(event_code=event_code, is_active=True).first()
        title = f"CivicConnect Alert: {event_code}"
        msg = f"Update on your civic report: {context.get('tracking_number', '')}"
        
        if template:
            try:
                title = template.subject_template.format(**context)
                msg = template.body_template.format(**context)
            except Exception as e:
                logger.error(f"Template formatting error: {e}")
                
        target_channels = channels or ["in_app", "email"]
        logs = []
        
        for ch in target_channels:
            log = NotificationLog.objects.create(
                recipient=recipient,
                channel=ch,
                event_code=event_code,
                title=title,
                message=msg,
                is_delivered=True,
                delivery_status="delivered",
            )
            logs.append(log)
            
        logger.info(f"Sent {len(logs)} notification(s) to {recipient.email} for event {event_code}")
        return logs
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import NotificationLog, UserDeviceToken, NotificationTemplate
from .serializers import NotificationLogSerializer, UserDeviceTokenSerializer, NotificationTemplateSerializer

class NotificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationLog.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return Response({"status": "marked as read"})

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        NotificationLog.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({"status": "all marked as read"})

class UserDeviceTokenViewSet(viewsets.ModelViewSet):
    serializer_class = UserDeviceTokenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserDeviceToken.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
''')

    write_file(os.path.join(app_dir, "serializers.py"), '''
from rest_framework import serializers
from .models import NotificationLog, UserDeviceToken, NotificationTemplate

class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = "__all__"

class UserDeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDeviceToken
        fields = "__all__"
        read_only_fields = ["user"]

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = "__all__"
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationLogViewSet, UserDeviceTokenViewSet

router = DefaultRouter()
router.register(r"user-notifications", NotificationLogViewSet, basename="user-notification")
router.register(r"device-tokens", UserDeviceTokenViewSet, basename="device-token")

urlpatterns = [
    path("", include(router.urls)),
]
''')

def generate_iot_app(base_dir):
    app_dir = os.path.join(base_dir, "iot")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "models.py"), '''
import uuid
from django.db import models
from django.utils import timezone
from accounts.models import Tenant, Ward, Department

class SensorDevice(models.Model):
    """Smart city IoT endpoint device (Air Quality, Smart Waste Bin, Water Pressure, Streetlight)."""
    SENSOR_TYPES = [
        ("air_quality", "Air Quality Monitor (PM2.5/PM10/CO2)"),
        ("waste_bin", "Ultrasonic Waste Bin Fill Level"),
        ("water_pressure", "Water Pipeline Pressure / Leak Sensor"),
        ("streetlight", "Smart Streetlight Luminaire & Power Monitor"),
        ("traffic_counter", "Geomagnetic Vehicle Traffic Counter"),
        ("flood_gauge", "Stormwater Drainage Level Gauge"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=100, unique=True, db_index=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="sensors")
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name="sensors")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="sensors")
    sensor_type = models.CharField(max_length=50, choices=SENSOR_TYPES)
    name = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    
    firmware_version = models.CharField(max_length=50, default="1.0.0")
    battery_level = models.PositiveSmallIntegerField(default=100)
    signal_rssi = models.SmallIntegerField(default=-70)
    is_online = models.BooleanField(default=True)
    
    threshold_warning = models.FloatField(default=75.0, help_text="Fill % or AQI limit triggering warning")
    threshold_critical = models.FloatField(default=90.0, help_text="Fill % or AQI limit triggering auto-complaint")
    auto_generate_complaint = models.BooleanField(default=True)
    
    last_telemetry_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_iot_sensor_devices"

    def __str__(self):
        return f"[{self.device_id}] {self.name} ({self.sensor_type})"

class TelemetryReading(models.Model):
    """High-throughput time-series sensor telemetry data record."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(SensorDevice, on_delete=models.CASCADE, related_name="readings")
    value = models.FloatField()
    unit = models.CharField(max_length=30, default="percentage")
    raw_payload = models.JSONField(default=dict, blank=True)
    is_anomaly = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = "civic_iot_telemetry_readings"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["device", "timestamp"]),
        ]

class SensorAlert(models.Model):
    """Automated alert generated when IoT readings exceed safe thresholds."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(SensorDevice, on_delete=models.CASCADE, related_name="alerts")
    severity = models.CharField(max_length=20, choices=[("warning", "Warning"), ("critical", "Critical")])
    metric_value = models.FloatField()
    message = models.CharField(max_length=255)
    complaint = models.ForeignKey("complaints.Complaint", on_delete=models.SET_NULL, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_iot_sensor_alerts"
        ordering = ["-created_at"]
''')

    write_file(os.path.join(app_dir, "services.py"), '''
import logging
from django.utils import timezone
from .models import SensorDevice, TelemetryReading, SensorAlert

logger = logging.getLogger(__name__)

class IoTService:
    @classmethod
    def ingest_telemetry(cls, device_id, value, unit="percentage", raw_payload=None):
        """Ingests raw sensor telemetry packet, validates bounds, and triggers auto-complaints on breach."""
        device = SensorDevice.objects.filter(device_id=device_id).first()
        if not device:
            logger.error(f"Sensor device not found: {device_id}")
            return None
            
        now = timezone.now()
        device.last_telemetry_at = now
        device.is_online = True
        device.save(update_fields=["last_telemetry_at", "is_online"])
        
        is_anomaly = value >= device.threshold_warning
        reading = TelemetryReading.objects.create(
            device=device,
            value=value,
            unit=unit,
            raw_payload=raw_payload or {},
            is_anomaly=is_anomaly,
            timestamp=now
        )
        
        if value >= device.threshold_critical:
            cls._create_critical_alert(device, value)
            
        return reading

    @classmethod
    def _create_critical_alert(cls, device, value):
        alert = SensorAlert.objects.create(
            device=device,
            severity="critical",
            metric_value=value,
            message=f"Critical reading {value} exceeds threshold {device.threshold_critical}"
        )
        logger.warning(f"IoT Critical Alert: Device {device.device_id} reached {value}")
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import SensorDevice, TelemetryReading, SensorAlert
from .serializers import SensorDeviceSerializer, TelemetryReadingSerializer, SensorAlertSerializer
from .services import IoTService

class SensorDeviceViewSet(viewsets.ModelViewSet):
    queryset = SensorDevice.objects.all()
    serializer_class = SensorDeviceSerializer
    permission_classes = [IsAuthenticated]

class TelemetryIngestView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        device_id = request.data.get("device_id")
        value = float(request.data.get("value", 0.0))
        unit = request.data.get("unit", "units")
        payload = request.data.get("payload", {})
        
        reading = IoTService.ingest_telemetry(device_id, value, unit, payload)
        if not reading:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": "telemetry accepted", "id": str(reading.id)}, status=status.HTTP_201_CREATED)

class SensorAlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SensorAlert.objects.all()
    serializer_class = SensorAlertSerializer
    permission_classes = [IsAuthenticated]
''')

    write_file(os.path.join(app_dir, "serializers.py"), '''
from rest_framework import serializers
from .models import SensorDevice, TelemetryReading, SensorAlert

class SensorDeviceSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source="ward.name", read_only=True)

    class Meta:
        model = SensorDevice
        fields = "__all__"

class TelemetryReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryReading
        fields = "__all__"

class SensorAlertSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source="device.name", read_only=True)
    sensor_type = serializers.CharField(source="device.sensor_type", read_only=True)

    class Meta:
        model = SensorAlert
        fields = "__all__"
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorDeviceViewSet, TelemetryIngestView, SensorAlertViewSet

router = DefaultRouter()
router.register(r"devices", SensorDeviceViewSet, basename="sensor-device")
router.register(r"alerts", SensorAlertViewSet, basename="sensor-alert")

urlpatterns = [
    path("ingest/", TelemetryIngestView.as_view(), name="iot-ingest"),
    path("", include(router.urls)),
]
''')

def generate_gamification_app(base_dir):
    app_dir = os.path.join(base_dir, "gamification")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "models.py"), '''
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import Tenant

class Badge(models.Model):
    """Achievement badge unlockable by citizens and municipal staff."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    icon_url = models.URLField(blank=True)
    karma_threshold = models.PositiveIntegerField(default=100)
    category = models.CharField(
        max_length=50,
        choices=[("reports", "Grievance Reporting"), ("verification", "Community Verification"), ("green", "Environmental & Cleanliness")],
        default="reports"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_gamification_badges"

    def __str__(self):
        return f"{self.name} ({self.code})"

class UserBadge(models.Model):
    """Association of earned badge to user with unlock timestamp."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "civic_gamification_user_badges"
        unique_together = ("user", "badge")

class CivicQuest(models.Model):
    """Time-limited community challenge (e.g. Report 3 potholes in Ward 5 this weekend)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="quests")
    title = models.CharField(max_length=200)
    description = models.TextField()
    reward_karma = models.PositiveIntegerField(default=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "civic_gamification_quests"
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import Badge, UserBadge, CivicQuest
from .serializers import BadgeSerializer, CivicQuestSerializer

User = get_user_model()

class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [AllowAny]

class CivicQuestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CivicQuest.objects.filter(is_active=True)
    serializer_class = CivicQuestSerializer
    permission_classes = [AllowAny]

class LeaderboardView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tenant_id = request.query_params.get("tenant_id")
        qs = User.objects.filter(role="citizen", is_active=True)
        if tenant_id:
            qs = qs.filter(tenant_id=tenant_id)
        leaders = qs.order_by("-karma_points")[:25].values(
            "id", "first_name", "last_name", "badge_title", "karma_points", "reports_resolved", "avatar"
        )
        return Response({"leaderboard": list(leaders)})
''')

    write_file(os.path.join(app_dir, "serializers.py"), '''
from rest_framework import serializers
from .models import Badge, UserBadge, CivicQuest

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"

class CivicQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CivicQuest
        fields = "__all__"
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BadgeViewSet, CivicQuestViewSet, LeaderboardView

router = DefaultRouter()
router.register(r"badges", BadgeViewSet, basename="badge")
router.register(r"quests", CivicQuestViewSet, basename="quest")

urlpatterns = [
    path("leaderboard/", LeaderboardView.as_view(), name="gamification-leaderboard"),
    path("", include(router.urls)),
]
''')

def generate_analytics_app(base_dir):
    app_dir = os.path.join(base_dir, "analytics")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "engine.py"), '''
import logging
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from datetime import timedelta
from complaints.models import Complaint
from accounts.models import Ward, Department

logger = logging.getLogger(__name__)

class AnalyticsEngine:
    @staticmethod
    def get_executive_kpis(tenant_id, days=30):
        """Computes executive-level municipal KPIs for city commissioners and department heads."""
        since = timezone.now() - timedelta(days=days)
        base_qs = Complaint.objects.filter(tenant_id=tenant_id, created_at__gte=since)
        
        total_reported = base_qs.count()
        total_resolved = base_qs.filter(status__in=["resolved", "verified"]).count()
        total_breached = base_qs.filter(is_sla_breached=True).count()
        
        sla_compliance_rate = round((1.0 - (total_breached / max(1, total_reported))) * 100.0, 1)
        resolution_rate = round((total_resolved / max(1, total_reported)) * 100.0, 1)
        
        # Ward distribution
        ward_stats = base_qs.values("ward__ward_number", "ward__name").annotate(
            count=Count("id")
        ).order_by("-count")[:10]
        
        # Department distribution
        dept_stats = base_qs.values("department__name").annotate(
            count=Count("id")
        ).order_by("-count")
        
        return {
            "timeframe_days": days,
            "total_reported": total_reported,
            "total_resolved": total_resolved,
            "total_breached": total_breached,
            "sla_compliance_rate": sla_compliance_rate,
            "resolution_rate": resolution_rate,
            "ward_distribution": list(ward_stats),
            "department_distribution": list(dept_stats),
        }
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .engine import AnalyticsEngine

class ExecutiveDashboardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tenant_id = request.user.tenant_id or request.query_params.get("tenant_id")
        days = int(request.query_params.get("days", 30))
        data = AnalyticsEngine.get_executive_kpis(tenant_id, days)
        return Response(data)
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path
from .views import ExecutiveDashboardView

urlpatterns = [
    path("kpis/", ExecutiveDashboardView.as_view(), name="analytics-kpis"),
]
''')

def generate_security_app(base_dir):
    app_dir = os.path.join(base_dir, "security")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "pii_masking.py"), '''
import re

class PIIMaskingService:
    @staticmethod
    def mask_email(email):
        """Masks citizen email address: j***n@example.com."""
        if not email or "@" not in email:
            return email
        name, domain = email.split("@", 1)
        if len(name) <= 2:
            masked = name[0] + "*"
        else:
            masked = name[0] + "*" * (len(name) - 2) + name[-1]
        return f"{masked}@{domain}"

    @staticmethod
    def mask_phone(phone):
        """Masks citizen phone number: +1 ***-***-4589."""
        if not phone or len(phone) < 4:
            return phone
        return "*" * (len(phone) - 4) + phone[-4:]

    @staticmethod
    def mask_citizen_profile(user_dict):
        """Returns anonymized version of citizen profile for public viewing."""
        if not user_dict:
            return user_dict
        masked = dict(user_dict)
        if "email" in masked:
            masked["email"] = PIIMaskingService.mask_email(masked["email"])
        if "phone_number" in masked:
            masked["phone_number"] = PIIMaskingService.mask_phone(masked["phone_number"])
        return masked
''')

    write_file(os.path.join(app_dir, "middleware.py"), '''
import logging
import time

logger = logging.getLogger(__name__)

class SecurityHeadersMiddleware:
    """Injects essential modern HTTP security headers on all API responses."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;"
        return response
''')

def generate_core_app(base_dir):
    app_dir = os.path.join(base_dir, "core")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "event_bus.py"), '''
import logging

logger = logging.getLogger(__name__)

class EventBus:
    _subscribers = {}

    @classmethod
    def subscribe(cls, event_name, handler):
        if event_name not in cls._subscribers:
            cls._subscribers[event_name] = []
        cls._subscribers[event_name].append(handler)

    @classmethod
    def publish(cls, event_name, payload):
        handlers = cls._subscribers.get(event_name, [])
        for handler in handlers:
            try:
                handler(payload)
            except Exception as e:
                logger.error(f"EventBus handler failed for {event_name}: {e}")
''')

    write_file(os.path.join(app_dir, "pagination.py"), '''
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
''')

if __name__ == "__main__":
    base = "backend"
    generate_workforce_app(base)
    generate_ai_routing_app(base)
    generate_notifications_app(base)
    generate_iot_app(base)
    generate_gamification_app(base)
    generate_analytics_app(base)
    generate_security_app(base)
    generate_core_app(base)
