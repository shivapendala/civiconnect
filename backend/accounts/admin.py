from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Municipality, Department, User, Role, Permission, UserRole,
    StaffProfile, CitizenProfile, Device, NotificationPreference,
    Notification, AuditLog, CivicPoints, Badge, CitizenBadge
)

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ("name", "state", "country", "contact_email", "contact_phone")
    search_fields = ("name", "state", "country")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "municipality", "manager")
    list_filter = ("municipality",)
    search_fields = ("name",)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "is_staff", "is_verified")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_verified")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename")

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role")

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "municipality", "department", "designation")
    list_filter = ("municipality", "department")

@admin.register(CitizenProfile)
class CitizenProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "municipality", "address")
    list_filter = ("municipality",)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("user", "device_type", "fcm_token")

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "push_enabled", "email_enabled", "sms_enabled")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read")
    list_filter = ("is_read",)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "entity_type", "entity_id", "created_at")
    list_filter = ("action", "entity_type")
    readonly_fields = ("created_at", "updated_at")

@admin.register(CivicPoints)
class CivicPointsAdmin(admin.ModelAdmin):
    list_display = ("citizen", "total_points", "level")

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "points_required")

@admin.register(CitizenBadge)
class CitizenBadgeAdmin(admin.ModelAdmin):
    list_display = ("citizen", "badge", "awarded_at")
