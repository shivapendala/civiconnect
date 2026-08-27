from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Tenant, Department, Ward, User, StaffSchedule, AuditLog

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "domain", "subscription_tier", "is_active", "created_at")
    list_filter = ("subscription_tier", "is_active", "country")
    search_fields = ("name", "code", "domain", "contact_email")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "tenant", "head_of_department", "sla_default_hours", "is_active")
    list_filter = ("tenant", "is_active")
    search_fields = ("name", "code")

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ("ward_number", "name", "tenant", "zone_name", "councillor_name", "population")
    list_filter = ("tenant", "is_active")
    search_fields = ("name", "councillor_name", "zone_name")

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "role", "tenant", "department", "karma_points", "is_active")
    list_filter = ("role", "tenant", "department", "is_active", "is_verified")
    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "avatar", "preferred_language")}),
        ("Municipal Affiliation", {"fields": ("role", "tenant", "department", "assigned_ward")}),
        ("Gamification & Stats", {"fields": ("karma_points", "badge_title", "reports_submitted", "reports_resolved")}),
        ("Permissions & Status", {"fields": ("is_active", "is_staff", "is_superuser", "is_verified", "is_mfa_enabled")}),
        ("Location", {"fields": ("last_location_lat", "last_location_lng", "last_location_updated")}),
    )

@admin.register(StaffSchedule)
class StaffScheduleAdmin(admin.ModelAdmin):
    list_display = ("user", "shift_date", "start_time", "end_time", "is_on_duty", "emergency_on_call")
    list_filter = ("shift_date", "is_on_duty", "emergency_on_call")

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "actor", "action", "entity_type", "entity_id", "tenant", "ip_address")
    list_filter = ("action", "entity_type", "timestamp")
    search_fields = ("actor__email", "entity_id", "ip_address")
    readonly_fields = [f.name for f in AuditLog._meta.fields]
