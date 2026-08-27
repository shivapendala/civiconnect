"""
Generator for CivicConnect Backend Apps:
- complaints
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
    print(f"Generated: {filepath} ({len(content.splitlines())} lines)")

def generate_complaints_app(base_dir):
    app_dir = os.path.join(base_dir, "complaints")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "models.py"), '''
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import Tenant, Department, Ward

class ComplaintCategory(models.Model):
    """Hierarchical taxonomy for municipal issues (e.g. Roads -> Pothole)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="categories")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="categories")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="subcategories")
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, default="alert-circle")
    color_code = models.CharField(max_length=20, default="#3b82f6")
    default_priority = models.CharField(
        max_length=20,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical Emergency")],
        default="medium",
    )
    sla_resolution_hours = models.PositiveIntegerField(default=48)
    sla_response_hours = models.PositiveIntegerField(default=4)
    requires_photo = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_complaint_categories"
        unique_together = ("tenant", "code")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class Complaint(models.Model):
    """Citizen grievance entity representing a reported civic issue."""
    STATUS_CHOICES = [
        ("submitted", "Submitted / New"),
        ("triaged", "Triaged & Validated"),
        ("assigned", "Assigned to Field Team"),
        ("in_progress", "Work In Progress"),
        ("resolved", "Resolved by Worker"),
        ("verified", "Citizen Verified & Closed"),
        ("rejected", "Rejected / Ineligible"),
        ("duplicate", "Marked as Duplicate"),
        ("escalated", "SLA Escalated"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low Priority"),
        ("medium", "Medium Priority"),
        ("high", "High Priority"),
        ("critical", "Critical Emergency"),
    ]

    CHANNEL_CHOICES = [
        ("mobile_app", "Mobile Application"),
        ("web_portal", "Citizen Web Portal"),
        ("whatsapp", "WhatsApp Bot"),
        ("phone_call", "Call Center / Helpline"),
        ("iot_sensor", "Automated IoT Telemetry"),
        ("field_officer", "Field Officer Ingestion"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_number = models.CharField(max_length=32, unique=True, db_index=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="complaints")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="complaints")
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name="complaints")
    category = models.ForeignKey(ComplaintCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="complaints")
    
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reported_complaints")
    assigned_worker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_jobs"
    )
    assigned_team = models.ForeignKey("workforce.FieldTeam", on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_complaints")
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="submitted", db_index=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium", db_index=True)
    intake_channel = models.CharField(max_length=30, choices=CHANNEL_CHOICES, default="mobile_app")
    
    # Geolocation data
    latitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, db_index=True)
    address_text = models.CharField(max_length=500, blank=True)
    landmark = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(max_length=20, blank=True)
    
    # SLA Tracking
    sla_response_due = models.DateTimeField(null=True, blank=True)
    sla_resolution_due = models.DateTimeField(null=True, blank=True, db_index=True)
    sla_responded_at = models.DateTimeField(null=True, blank=True)
    sla_resolved_at = models.DateTimeField(null=True, blank=True)
    is_sla_breached = models.BooleanField(default=False, db_index=True)
    sla_breach_level = models.PositiveSmallIntegerField(default=0)
    
    # AI Triage & Verification
    ai_confidence_score = models.FloatField(default=0.0)
    ai_predicted_category = models.CharField(max_length=150, blank=True)
    ai_severity_score = models.FloatField(default=0.0)
    ai_duplicate_cluster_id = models.CharField(max_length=100, blank=True)
    duplicate_of = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="duplicates")
    
    # Citizen Engagement & Community
    upvotes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)
    citizen_feedback_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    citizen_feedback_notes = models.TextField(blank=True)
    
    # Resolution details
    resolution_notes = models.TextField(blank=True)
    resolution_proof_image = models.ImageField(upload_to="resolutions/%Y/%m/", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "civic_complaints"
        indexes = [
            models.Index(fields=["tenant", "status"]),
            models.Index(fields=["department", "status"]),
            models.Index(fields=["ward", "status"]),
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.tracking_number}] {self.title} - {self.status}"

    @property
    def is_resolved_or_closed(self):
        return self.status in ["resolved", "verified", "rejected", "duplicate"]

    @property
    def hours_remaining(self):
        if not self.sla_resolution_due or self.is_resolved_or_closed:
            return 0
        diff = self.sla_resolution_due - timezone.now()
        return round(diff.total_seconds() / 3600.0, 1)

class ComplaintAttachment(models.Model):
    """Media evidence (photos, videos, audio notes) attached to a complaint."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="attachments")
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="complaint_attachments/%Y/%m/")
    file_type = models.CharField(max_length=50, choices=[("image", "Image"), ("video", "Video"), ("audio", "Audio Voice Note"), ("document", "Document")])
    is_resolution_proof = models.BooleanField(default=False)
    ai_analyzed = models.BooleanField(default=False)
    ai_labels = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_complaint_attachments"

class ComplaintComment(models.Model):
    """Interactive updates and comments on a grievance."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    is_internal_staff_note = models.BooleanField(default=False)
    attachment = models.FileField(upload_to="comment_attachments/%Y/%m/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_complaint_comments"
        ordering = ["created_at"]

class ComplaintVote(models.Model):
    """Community endorsements/upvotes for neighborhood complaints."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_complaint_votes"
        unique_together = ("complaint", "user")

class StatusTransitionLog(models.Model):
    """Auditable state machine log for complaint lifecycle transitions."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="status_history")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    from_status = models.CharField(max_length=30)
    to_status = models.CharField(max_length=30)
    reason = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "civic_status_transition_logs"
        ordering = ["-timestamp"]
''')

    write_file(os.path.join(app_dir, "services.py"), '''
import logging
import secrets
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Complaint, ComplaintCategory, StatusTransitionLog, ComplaintVote
from accounts.models import AuditLog

logger = logging.getLogger(__name__)

class ComplaintService:
    @staticmethod
    def generate_tracking_number(tenant_code="CIVIC"):
        """Generates human-readable grievance identifier e.g. CIV-2026-X892F."""
        year = timezone.now().year
        rand = secrets.token_hex(3).upper()
        return f"{tenant_code[:3]}-{year}-{rand}"

    @classmethod
    @transaction.atomic
    def create_complaint(cls, citizen, title, description, category_id, latitude, longitude, **kwargs):
        """Creates a new complaint with SLA deadline calculations and automated tracking number."""
        category = ComplaintCategory.objects.get(id=category_id)
        tenant = category.tenant
        tracking = cls.generate_tracking_number(tenant.code)
        
        now = timezone.now()
        response_due = now + timedelta(hours=category.sla_response_hours)
        resolution_due = now + timedelta(hours=category.sla_resolution_hours)
        
        complaint = Complaint.objects.create(
            tracking_number=tracking,
            tenant=tenant,
            department=category.department,
            category=category,
            citizen=citizen,
            title=title,
            description=description,
            priority=category.default_priority,
            latitude=latitude,
            longitude=longitude,
            sla_response_due=response_due,
            sla_resolution_due=resolution_due,
            **kwargs
        )
        
        # Log initial creation transition
        StatusTransitionLog.objects.create(
            complaint=complaint,
            actor=citizen,
            from_status="none",
            to_status="submitted",
            reason="Complaint lodged by citizen",
        )
        
        # Increment citizen stats
        citizen.reports_submitted += 1
        citizen.karma_points += 10
        citizen.save(update_fields=["reports_submitted", "karma_points"])
        
        logger.info(f"Complaint {complaint.tracking_number} created by {citizen.email}")
        return complaint

    @staticmethod
    @transaction.atomic
    def transition_status(complaint, new_status, actor, reason=""):
        """Transitions complaint lifecycle status with audit logging and milestone tracking."""
        old_status = complaint.status
        if old_status == new_status:
            return complaint
            
        complaint.status = new_status
        now = timezone.now()
        
        if new_status in ["triaged", "assigned"] and not complaint.sla_responded_at:
            complaint.sla_responded_at = now
            
        if new_status == "resolved":
            complaint.sla_resolved_at = now
            if complaint.sla_resolution_due and now > complaint.sla_resolution_due:
                complaint.is_sla_breached = True
            if complaint.assigned_worker:
                complaint.assigned_worker.reports_resolved += 1
                complaint.assigned_worker.save(update_fields=["reports_resolved"])
                
        if new_status == "verified":
            complaint.citizen.karma_points += 20
            complaint.citizen.save(update_fields=["karma_points"])
            
        complaint.save()
        
        StatusTransitionLog.objects.create(
            complaint=complaint,
            actor=actor,
            from_status=old_status,
            to_status=new_status,
            reason=reason,
        )
        
        logger.info(f"Complaint {complaint.tracking_number} transitioned from {old_status} -> {new_status} by {actor}")
        return complaint

    @staticmethod
    def toggle_vote(complaint, user):
        """Allows citizens to upvote/endorse an issue."""
        vote, created = ComplaintVote.objects.get_or_create(complaint=complaint, user=user)
        if not created:
            vote.delete()
            complaint.upvotes_count = max(0, complaint.upvotes_count - 1)
            complaint.save(update_fields=["upvotes_count"])
            return False
        else:
            complaint.upvotes_count += 1
            complaint.save(update_fields=["upvotes_count"])
            return True
''')

    write_file(os.path.join(app_dir, "serializers.py"), '''
from rest_framework import serializers
from .models import Complaint, ComplaintCategory, ComplaintAttachment, ComplaintComment, ComplaintVote, StatusTransitionLog

class ComplaintCategorySerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = ComplaintCategory
        fields = [
            "id", "tenant", "department", "department_name", "parent", "name", "code",
            "description", "icon_name", "color_code", "default_priority",
            "sla_resolution_hours", "sla_response_hours", "requires_photo", "is_active"
        ]

class ComplaintAttachmentSerializer(serializers.ModelSerializer):
    uploader_name = serializers.CharField(source="uploader.get_full_name", read_only=True)

    class Meta:
        model = ComplaintAttachment
        fields = ["id", "file", "file_type", "uploader", "uploader_name", "is_resolution_proof", "ai_analyzed", "ai_labels", "created_at"]

class ComplaintCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    author_role = serializers.CharField(source="author.role", read_only=True)

    class Meta:
        model = ComplaintComment
        fields = ["id", "complaint", "author", "author_name", "author_role", "content", "is_internal_staff_note", "attachment", "created_at"]

class StatusTransitionLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source="actor.get_full_name", read_only=True)

    class Meta:
        model = StatusTransitionLog
        fields = ["id", "from_status", "to_status", "actor", "actor_name", "reason", "timestamp"]

class ComplaintListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    ward_name = serializers.CharField(source="ward.name", read_only=True)
    citizen_name = serializers.CharField(source="citizen.get_full_name", read_only=True)
    assigned_worker_name = serializers.CharField(source="assigned_worker.get_full_name", read_only=True)
    hours_remaining = serializers.FloatField(read_only=True)

    class Meta:
        model = Complaint
        fields = [
            "id", "tracking_number", "title", "status", "priority", "intake_channel",
            "category", "category_name", "department", "department_name", "ward", "ward_name",
            "citizen", "citizen_name", "assigned_worker", "assigned_worker_name",
            "latitude", "longitude", "address_text", "upvotes_count", "comments_count",
            "is_sla_breached", "hours_remaining", "created_at", "sla_resolution_due"
        ]

class ComplaintDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    ward_name = serializers.CharField(source="ward.name", read_only=True)
    citizen_name = serializers.CharField(source="citizen.get_full_name", read_only=True)
    assigned_worker_name = serializers.CharField(source="assigned_worker.get_full_name", read_only=True)
    attachments = ComplaintAttachmentSerializer(many=True, read_only=True)
    comments = ComplaintCommentSerializer(many=True, read_only=True)
    status_history = StatusTransitionLogSerializer(many=True, read_only=True)
    hours_remaining = serializers.FloatField(read_only=True)

    class Meta:
        model = Complaint
        fields = "__all__"

class ComplaintCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = [
            "title", "description", "category", "ward", "latitude", "longitude",
            "address_text", "landmark", "pincode", "intake_channel", "is_public"
        ]
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Complaint, ComplaintCategory, ComplaintAttachment, ComplaintComment, StatusTransitionLog
from .serializers import (
    ComplaintListSerializer, ComplaintDetailSerializer, ComplaintCreateSerializer,
    ComplaintCategorySerializer, ComplaintAttachmentSerializer, ComplaintCommentSerializer
)
from .services import ComplaintService
from accounts.permissions import IsMunicipalAdmin, IsStaffOrFieldWorker

class ComplaintCategoryViewSet(viewsets.ModelViewSet):
    queryset = ComplaintCategory.objects.filter(is_active=True)
    serializer_class = ComplaintCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["tenant", "department", "parent"]
    search_fields = ["name", "code", "description"]

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all().select_related("tenant", "department", "ward", "category", "citizen", "assigned_worker")
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "priority", "department", "ward", "tenant", "is_sla_breached", "intake_channel"]
    search_fields = ["tracking_number", "title", "description", "address_text"]
    ordering_fields = ["created_at", "sla_resolution_due", "priority", "upvotes_count"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return ComplaintCreateSerializer
        if self.action in ["retrieve", "update", "partial_update"]:
            return ComplaintDetailSerializer
        return ComplaintListSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "super_admin":
            return qs
        if user.role == "citizen":
            return qs.filter(citizen=user)
        if user.is_field_staff and user.role == "field_worker":
            return qs.filter(assigned_worker=user)
        if user.tenant:
            return qs.filter(tenant=user.tenant)
        return qs

    def perform_create(self, serializer):
        data = serializer.validated_data
        complaint = ComplaintService.create_complaint(
            citizen=self.request.user,
            title=data.get("title"),
            description=data.get("description"),
            category_id=data.get("category").id,
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            ward=data.get("ward"),
            address_text=data.get("address_text", ""),
            landmark=data.get("landmark", ""),
            pincode=data.get("pincode", ""),
            intake_channel=data.get("intake_channel", "mobile_app"),
            is_public=data.get("is_public", True),
        )
        serializer.instance = complaint

    @action(detail=True, methods=["post"], permission_classes=[IsStaffOrFieldWorker])
    def transition(self, request, pk=None):
        complaint = self.get_object()
        new_status = request.data.get("status")
        reason = request.data.get("reason", "")
        if not new_status:
            return Response({"error": "Target status required"}, status=status.HTTP_400_BAD_REQUEST)
        updated = ComplaintService.transition_status(complaint, new_status, request.user, reason)
        return Response(ComplaintDetailSerializer(updated).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        complaint = self.get_object()
        voted = ComplaintService.toggle_vote(complaint, request.user)
        return Response({"voted": voted, "upvotes_count": complaint.upvotes_count})

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        complaint = self.get_object()
        content = request.data.get("content")
        is_internal = request.data.get("is_internal", False)
        if not content:
            return Response({"error": "Content required"}, status=status.HTTP_400_BAD_REQUEST)
        comment = ComplaintComment.objects.create(
            complaint=complaint,
            author=request.user,
            content=content,
            is_internal_staff_note=is_internal,
        )
        complaint.comments_count += 1
        complaint.save(update_fields=["comments_count"])
        return Response(ComplaintCommentSerializer(comment).data, status=status.HTTP_201_CREATED)

class ComplaintAttachmentViewSet(viewsets.ModelViewSet):
    queryset = ComplaintAttachment.objects.all()
    serializer_class = ComplaintAttachmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet, ComplaintCategoryViewSet, ComplaintAttachmentViewSet

router = DefaultRouter()
router.register(r"categories", ComplaintCategoryViewSet, basename="category")
router.register(r"attachments", ComplaintAttachmentViewSet, basename="attachment")
router.register(r"", ComplaintViewSet, basename="complaint")

urlpatterns = [
    path("", include(router.urls)),
]
''')

if __name__ == "__main__":
    generate_complaints_app("backend")
