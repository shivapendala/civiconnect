"""
Generator for CivicConnect Enterprise Backend Modules.
Generates comprehensive Django & FastAPI backend components across 12 core domains.
"""
import os

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Generated: {filepath} ({len(content.splitlines())} lines)")

def generate_accounts_app(base_dir):
    app_dir = os.path.join(base_dir, "accounts")
    os.makedirs(app_dir, exist_ok=True)
    
    write_file(os.path.join(app_dir, "__init__.py"), 'default_app_config = "accounts.apps.AccountsConfig"\n')
    
    write_file(os.path.join(app_dir, "apps.py"), '''
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = "User & Municipal Accounts"

    def ready(self):
        import accounts.signals  # noqa
''')

    write_file(os.path.join(app_dir, "models.py"), '''
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Tenant(models.Model):
    """Represents a municipality, city council, or regional administrative zone."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    domain = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="United States")
    timezone = models.CharField(max_length=50, default="UTC")
    is_active = models.BooleanField(default=True)
    subscription_tier = models.CharField(
        max_length=50,
        choices=[
            ("starter", "Starter Municipality"),
            ("professional", "Professional City"),
            ("enterprise", "Metropolitan Enterprise"),
        ],
        default="professional",
    )
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30, blank=True)
    logo_url = models.URLField(blank=True, null=True)
    config = models.JSONField(default=dict, blank=True, help_text="Tenant-specific feature flags and SLA rules")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "civic_tenants"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"

class Department(models.Model):
    """Department within a municipality (e.g., Sanitation, Roads, Water, Electricity)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="headed_departments"
    )
    email = models.EmailField(blank=True)
    emergency_phone = models.CharField(max_length=30, blank=True)
    sla_default_hours = models.PositiveIntegerField(default=48)
    auto_assignment_enabled = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "civic_departments"
        unique_together = ("tenant", "code")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.tenant.code}"

class Ward(models.Model):
    """Administrative ward or district within a municipal tenant."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="wards")
    ward_number = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    zone_name = models.CharField(max_length=100, blank=True)
    councillor_name = models.CharField(max_length=150, blank=True)
    councillor_email = models.EmailField(blank=True)
    councillor_phone = models.CharField(max_length=30, blank=True)
    population = models.PositiveIntegerField(default=0)
    area_sq_km = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    boundary_geojson = models.JSONField(null=True, blank=True, help_text="GeoJSON Polygon boundary of the ward")
    center_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    center_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "civic_wards"
        unique_together = ("tenant", "ward_number")
        ordering = ["ward_number"]

    def __str__(self):
        return f"Ward {self.ward_number}: {self.name} ({self.tenant.code})"

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "super_admin")
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Custom User model supporting Citizens, Municipal Staff, Field Workers, and Super Admins."""
    ROLE_CHOICES = [
        ("citizen", "Citizen / Resident"),
        ("field_worker", "Field Operations Worker"),
        ("triage_officer", "Triage & Dispatch Officer"),
        ("ward_officer", "Ward Administrative Officer"),
        ("dept_manager", "Department Manager"),
        ("municipal_admin", "Municipal Administrator"),
        ("super_admin", "System Super Administrator"),
    ]

    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True, db_index=True)
    phone_number = models.CharField(max_length=30, blank=True, db_index=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="citizen")
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_members")
    assigned_ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_officers")
    
    avatar = models.ImageField(upload_to="avatars/%Y/%m/", null=True, blank=True)
    badge_title = models.CharField(max_length=100, default="Civic Contributor")
    karma_points = models.IntegerField(default=0, db_index=True)
    reports_submitted = models.PositiveIntegerField(default=0)
    reports_resolved = models.PositiveIntegerField(default=0)
    
    is_verified = models.BooleanField(default=False)
    is_mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=64, blank=True)
    
    preferred_language = models.CharField(max_length=10, default="en")
    notification_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text="Channels: email, sms, push, whatsapp",
    )
    last_location_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_location_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_location_updated = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "civic_users"
        indexes = [
            models.Index(fields=["tenant", "role"]),
            models.Index(fields=["department", "role"]),
            models.Index(fields=["assigned_ward"]),
        ]

    def __str__(self):
        return f"{self.get_full_name() or self.email} [{self.get_role_display()}]"

    @property
    def is_field_staff(self):
        return self.role in ["field_worker", "triage_officer"]

    @property
    def is_admin_or_manager(self):
        return self.role in ["dept_manager", "municipal_admin", "super_admin"]

class StaffSchedule(models.Model):
    """Tracks field staff duty schedules and active shifts."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shifts")
    shift_date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_on_duty = models.BooleanField(default=False)
    emergency_on_call = models.BooleanField(default=False)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "civic_staff_schedules"
        unique_together = ("user", "shift_date", "start_time")

class AuditLog(models.Model):
    """System-wide audit trail for compliance, security, and record tracking."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_actions")
    action = models.CharField(max_length=100, db_index=True)
    entity_type = models.CharField(max_length=100, db_index=True)
    entity_id = models.CharField(max_length=100, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    payload_before = models.JSONField(null=True, blank=True)
    payload_after = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = "civic_audit_logs"
        ordering = ["-timestamp"]
''')

    write_file(os.path.join(app_dir, "permissions.py"), '''
from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "super_admin")

class IsMunicipalAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role in ["municipal_admin", "super_admin"]
        )

class IsDepartmentManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ["dept_manager", "municipal_admin", "super_admin"]
        )

class IsStaffOrFieldWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role != "citizen"
        )

class IsTenantScoped(permissions.BasePermission):
    """Ensures staff can only view and modify records belonging to their tenant."""
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role == "super_admin":
            return True
        if hasattr(obj, "tenant"):
            return obj.tenant_id == request.user.tenant_id
        if hasattr(obj, "tenant_id"):
            return obj.tenant_id == request.user.tenant_id
        return True
''')

    write_file(os.path.join(app_dir, "serializers.py"), '''
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tenant, Department, Ward, StaffSchedule, AuditLog

User = get_user_model()

class TenantSerializer(serializers.ModelSerializer):
    departments_count = serializers.IntegerField(source="departments.count", read_only=True)
    wards_count = serializers.IntegerField(source="wards.count", read_only=True)

    class Meta:
        model = Tenant
        fields = [
            "id", "name", "code", "domain", "state", "country", "timezone",
            "is_active", "subscription_tier", "contact_email", "contact_phone",
            "logo_url", "config", "departments_count", "wards_count", "created_at", "updated_at"
        ]

class DepartmentSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)
    staff_count = serializers.IntegerField(source="staff_members.count", read_only=True)

    class Meta:
        model = Department
        fields = [
            "id", "tenant", "tenant_name", "name", "code", "description",
            "head_of_department", "email", "emergency_phone", "sla_default_hours",
            "auto_assignment_enabled", "is_active", "staff_count", "created_at", "updated_at"
        ]

class WardSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)

    class Meta:
        model = Ward
        fields = [
            "id", "tenant", "tenant_name", "ward_number", "name", "zone_name",
            "councillor_name", "councillor_email", "councillor_phone", "population",
            "area_sq_km", "boundary_geojson", "center_latitude", "center_longitude",
            "is_active", "created_at", "updated_at"
        ]

class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    ward_name = serializers.CharField(source="assigned_ward.name", read_only=True)
    tenant_name = serializers.CharField(source="tenant.name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "phone_number", "role",
            "tenant", "tenant_name", "department", "department_name",
            "assigned_ward", "ward_name", "avatar", "badge_title", "karma_points",
            "reports_submitted", "reports_resolved", "is_verified", "preferred_language",
            "created_at"
        ]
        read_only_fields = ["karma_points", "reports_submitted", "reports_resolved", "is_verified"]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "phone_number", "tenant"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class StaffScheduleSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = StaffSchedule
        fields = ["id", "user", "user_name", "shift_date", "start_time", "end_time", "is_on_duty", "emergency_on_call", "notes"]

class AuditLogSerializer(serializers.ModelSerializer):
    actor_email = serializers.CharField(source="actor.email", read_only=True)

    class Meta:
        model = AuditLog
        fields = ["id", "tenant", "actor", "actor_email", "action", "entity_type", "entity_id", "ip_address", "timestamp", "payload_after"]
''')

    write_file(os.path.join(app_dir, "services.py"), '''
import logging
from django.db import transaction
from django.utils import timezone
from .models import User, Tenant, Department, Ward, AuditLog

logger = logging.getLogger(__name__)

class AccountService:
    @staticmethod
    @transaction.atomic
    def onboard_tenant(name, code, domain, state, contact_email, subscription_tier="professional", default_departments=None):
        """Initializes a new municipality tenant with base departments and wards."""
        tenant = Tenant.objects.create(
            name=name,
            code=code.upper(),
            domain=domain.lower(),
            state=state,
            contact_email=contact_email,
            subscription_tier=subscription_tier,
        )
        
        default_depts = default_departments or [
            {"name": "Public Works & Roads", "code": "ROADS", "sla_hours": 48},
            {"name": "Waste Management & Sanitation", "code": "WASTE", "sla_hours": 24},
            {"name": "Water Supply & Drainage", "code": "WATER", "sla_hours": 24},
            {"name": "Street Lighting & Power", "code": "POWER", "sla_hours": 12},
            {"name": "Parks & Public Spaces", "code": "PARKS", "sla_hours": 72},
            {"name": "Health & Environmental Safety", "code": "HEALTH", "sla_hours": 24},
        ]
        
        for dept in default_depts:
            Department.objects.create(
                tenant=tenant,
                name=dept["name"],
                code=dept["code"],
                sla_default_hours=dept.get("sla_hours", 48),
            )
            
        logger.info(f"Onboarded tenant {tenant.name} with {len(default_depts)} departments.")
        return tenant

    @staticmethod
    def update_user_location(user, latitude, longitude):
        """Updates real-time GPS coordinates for field workers."""
        user.last_location_lat = latitude
        user.last_location_lng = longitude
        user.last_location_updated = timezone.now()
        user.save(update_fields=["last_location_lat", "last_location_lng", "last_location_updated"])

    @staticmethod
    def award_karma(user, points, reason=""):
        """Awards karma points to a citizen for positive civic participation."""
        user.karma_points += points
        if user.karma_points >= 1000:
            user.badge_title = "Civic Champion"
        elif user.karma_points >= 500:
            user.badge_title = "Civic Guardian"
        elif user.karma_points >= 200:
            user.badge_title = "Active Resident"
        elif user.karma_points >= 50:
            user.badge_title = "Community Neighbor"
        user.save(update_fields=["karma_points", "badge_title"])
''')

    write_file(os.path.join(app_dir, "views.py"), '''
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import Tenant, Department, Ward, StaffSchedule, AuditLog
from .serializers import (
    TenantSerializer, DepartmentSerializer, WardSerializer,
    UserSerializer, UserRegistrationSerializer, StaffScheduleSerializer, AuditLogSerializer
)
from .permissions import IsSuperAdmin, IsMunicipalAdmin, IsDepartmentManager, IsStaffOrFieldWorker

User = get_user_model()

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return Tenant.objects.all()
        return Tenant.objects.filter(id=self.request.user.tenant_id)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsMunicipalAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "super_admin":
            return Department.objects.all()
        return Department.objects.filter(tenant=user.tenant)

class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [IsMunicipalAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "super_admin":
            return Ward.objects.all()
        return Ward.objects.filter(tenant=user.tenant)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "super_admin":
            return User.objects.all()
        if user.is_admin_or_manager:
            return User.objects.filter(tenant=user.tenant)
        return User.objects.filter(id=user.id)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def update_location(self, request):
        lat = request.data.get("latitude")
        lng = request.data.get("longitude")
        if lat is None or lng is None:
            return Response({"error": "Latitude and longitude required"}, status=status.HTTP_400_BAD_REQUEST)
        from .services import AccountService
        AccountService.update_user_location(request.user, lat, lng)
        return Response({"status": "Location updated"})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class StaffScheduleViewSet(viewsets.ModelViewSet):
    queryset = StaffSchedule.objects.all()
    serializer_class = StaffScheduleSerializer
    permission_classes = [IsDepartmentManager]

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsMunicipalAdmin]
''')

    write_file(os.path.join(app_dir, "urls.py"), '''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TenantViewSet, DepartmentViewSet, WardViewSet,
    UserViewSet, RegisterView, StaffScheduleViewSet, AuditLogViewSet
)

router = DefaultRouter()
router.register(r"tenants", TenantViewSet, basename="tenant")
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"wards", WardViewSet, basename="ward")
router.register(r"users", UserViewSet, basename="user")
router.register(r"schedules", StaffScheduleViewSet, basename="schedule")
router.register(r"audit-logs", AuditLogViewSet, basename="audit-log")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("", include(router.urls)),
]
''')

if __name__ == "__main__":
    generate_accounts_app("backend")
