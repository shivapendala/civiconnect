from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import AbstractBaseModel

class Role(AbstractBaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Permission(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Department(AbstractBaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey('StaffProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments')

    def __str__(self):
        return self.name

class User(AbstractUser, AbstractBaseModel):
    # Using AbstractUser gives us password hashing, auth flows, etc.
    # We remove default username in favor of email if needed, but keeping it simple for now.
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserRole(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

class StaffProfile(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='staff')
    designation = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.email} - Staff"

class CitizenProfile(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='citizen_profile')
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.email} - Citizen"

class Device(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    fcm_token = models.CharField(max_length=255, blank=True)
    device_type = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"Device for {self.user.email}"

class NotificationPreference(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    push_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"Preferences for {self.user.email}"

class Notification(AbstractBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    # Generic relation to complaint or other entity without hard dependency
    reference_id = models.CharField(max_length=100, blank=True) 
    
    def __str__(self):
        return f"Notification to {self.user.email}: {self.title}"
