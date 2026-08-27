from django.db import models
from core.models import AbstractBaseModel
from accounts.models import Department, StaffProfile, CitizenProfile

class ComplaintCategory(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class ComplaintPriority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    CRITICAL = 'CRITICAL', 'Critical'

class ComplaintStatus(models.TextChoices):
    SUBMITTED = 'SUBMITTED', 'Submitted'
    ACKNOWLEDGED = 'ACKNOWLEDGED', 'Acknowledged'
    ASSIGNED = 'ASSIGNED', 'Assigned'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    ON_HOLD = 'ON_HOLD', 'On Hold'
    RESOLVED = 'RESOLVED', 'Resolved'
    CITIZEN_VERIFIED = 'CITIZEN_VERIFIED', 'Citizen Verified'
    CLOSED = 'CLOSED', 'Closed'
    REJECTED = 'REJECTED', 'Rejected'
    REOPENED = 'REOPENED', 'Reopened'
    ESCALATED = 'ESCALATED', 'Escalated'

class Complaint(AbstractBaseModel):
    citizen = models.ForeignKey(CitizenProfile, on_delete=models.CASCADE, related_name='complaints')
    municipality = models.ForeignKey('accounts.Municipality', on_delete=models.CASCADE, related_name='complaints', null=True)
    category = models.ForeignKey(ComplaintCategory, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=ComplaintPriority.choices, default=ComplaintPriority.MEDIUM)
    status = models.CharField(max_length=20, choices=ComplaintStatus.choices, default=ComplaintStatus.SUBMITTED)
    ai_confidence_score = models.FloatField(default=0.0)
    ai_insights = models.JSONField(null=True, blank=True, help_text="AI generated insights, similar complaints, and analysis")
    
    def __str__(self):
        return self.title

class ChatMessage(AbstractBaseModel):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Msg on {self.complaint.id} by {self.sender.email}"

class ComplaintLocation(AbstractBaseModel):
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField(blank=True)

class ComplaintAttachment(AbstractBaseModel):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='attachments')
    file_url = models.URLField()
    file_type = models.CharField(max_length=50) # image/video
    
class ComplaintAssignment(AbstractBaseModel):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='assignments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    staff = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    
class Investigation(AbstractBaseModel):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='investigations')
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    notes = models.TextField()

class Resolution(AbstractBaseModel):
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='resolution')
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    summary = models.TextField()
    resolved_at = models.DateTimeField(auto_now_add=True)

class ResolutionEvidence(AbstractBaseModel):
    resolution = models.ForeignKey(Resolution, on_delete=models.CASCADE, related_name='evidence')
    file_url = models.URLField()
    description = models.TextField(blank=True)

class Feedback(AbstractBaseModel):
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='feedback')
    citizen = models.ForeignKey(CitizenProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField(blank=True)

class SLARule(AbstractBaseModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sla_rules')
    priority = models.CharField(max_length=20, choices=ComplaintPriority.choices)
    resolution_time_hours = models.IntegerField(help_text="Expected resolution time in hours")

class PerformanceMetrics(AbstractBaseModel):
    department = models.OneToOneField(Department, on_delete=models.CASCADE, related_name='performance_metrics')
    total_complaints_handled = models.IntegerField(default=0)
    average_resolution_time_hours = models.FloatField(default=0.0)
    sla_compliance_rate = models.FloatField(default=0.0)
