import logging
from .models import User, Notification, NotificationPreference

logger = logging.getLogger(__name__)

def send_notification(user_id, title, body, reference_id=""):
    """
    Sends a notification to a user based on their preferences.
    """
    try:
        user = User.objects.get(id=user_id)
        prefs, _ = NotificationPreference.objects.get_or_create(user=user)
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found for notification.")
        return False

    # 1. Always save in-app notification
    Notification.objects.create(
        user=user,
        title=title,
        body=body,
        reference_id=reference_id
    )

    # 2. Push Notification
    if prefs.push_enabled:
        # Mock Firebase Cloud Messaging (FCM) dispatch
        logger.info(f"[FCM PUSH] To: {user.email} | Title: {title} | Body: {body}")
        
    # 3. Email Notification
    if prefs.email_enabled:
        # Mock Django send_mail
        logger.info(f"[EMAIL] To: {user.email} | Subject: {title} | Body: {body}")
        
    # 4. SMS Notification
    if prefs.sms_enabled and user.phone_number:
        # Mock Twilio SMS
        logger.info(f"[SMS] To: {user.phone_number} | Msg: {title} - {body}")

    return True

# Example triggers:
# send_notification(citizen.user.id, "Complaint Submitted", "Your complaint CC-123 has been received.")
# send_notification(staff.user.id, "New Assignment", "You have been assigned to CC-123.")
