import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Tenant, AuditLog

User = get_user_model()
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New user registered: {instance.email} with role {instance.role}")
        # Automatically assign default avatar and initial karma welcome bonus
        if instance.role == "citizen" and instance.karma_points == 0:
            instance.karma_points = 25
            instance.save(update_fields=["karma_points"])
