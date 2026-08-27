from django.contrib import admin
from .models import (
    ComplaintCategory, Complaint, ChatMessage, ComplaintLocation,
    ComplaintAttachment, ComplaintAssignment, Investigation,
    Resolution, ResolutionEvidence, Feedback, SLARule, PerformanceMetrics
)

@admin.register(ComplaintCategory)
class ComplaintCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "description")
    search_fields = ("name", "description")
    list_filter = ("department",)

class ComplaintLocationInline(admin.StackedInline):
    model = ComplaintLocation
    extra = 0

class ComplaintAttachmentInline(admin.TabularInline):
    model = ComplaintAttachment
    extra = 0

class ComplaintAssignmentInline(admin.TabularInline):
    model = ComplaintAssignment
    extra = 0

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("title", "citizen", "category", "municipality", "priority", "status", "ai_confidence_score", "created_at")
    list_filter = ("status", "priority", "category", "municipality")
    search_fields = ("title", "description", "citizen__user__email")
    inlines = [ComplaintLocationInline, ComplaintAttachmentInline, ComplaintAssignmentInline]
    readonly_fields = ("created_at", "updated_at")

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("complaint", "sender", "content", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("content", "sender__email", "complaint__title")

@admin.register(ComplaintLocation)
class ComplaintLocationAdmin(admin.ModelAdmin):
    list_display = ("complaint", "latitude", "longitude", "address")
    search_fields = ("address", "complaint__title")

@admin.register(ComplaintAttachment)
class ComplaintAttachmentAdmin(admin.ModelAdmin):
    list_display = ("complaint", "file_type", "file_url")

@admin.register(ComplaintAssignment)
class ComplaintAssignmentAdmin(admin.ModelAdmin):
    list_display = ("complaint", "department", "staff", "assigned_at")
    list_filter = ("department", "assigned_at")

@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ("complaint", "staff", "created_at")
    search_fields = ("notes", "complaint__title")

@admin.register(Resolution)
class ResolutionAdmin(admin.ModelAdmin):
    list_display = ("complaint", "staff", "summary", "resolved_at")
    search_fields = ("summary", "complaint__title")

@admin.register(ResolutionEvidence)
class ResolutionEvidenceAdmin(admin.ModelAdmin):
    list_display = ("resolution", "file_url", "description")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("complaint", "citizen", "rating", "comments")
    list_filter = ("rating",)

@admin.register(SLARule)
class SLARuleAdmin(admin.ModelAdmin):
    list_display = ("department", "priority", "resolution_time_hours")
    list_filter = ("department", "priority")

@admin.register(PerformanceMetrics)
class PerformanceMetricsAdmin(admin.ModelAdmin):
    list_display = ("department", "total_complaints_handled", "average_resolution_time_hours", "sla_compliance_rate")
