import logging
from .models import AuditLog, User

logger = logging.getLogger(__name__)

def log_audit_action(user_id, action, entity_type, entity_id, old_value="", new_value="", ip_address=None):
    """
    Records an action into the system Audit Log.
    
    :param user_id: ID of the user performing the action (None if SYSTEM).
    :param action: A string describing the action (e.g. 'Changed Status', 'Login', 'Deleted').
    :param entity_type: The model/type affected (e.g. 'Complaint', 'Department').
    :param entity_id: The ID of the affected entity.
    :param old_value: String representation of the previous state.
    :param new_value: String representation of the new state.
    :param ip_address: The IP address of the user (if available via request).
    """
    user = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass

    log_entry = AuditLog.objects.create(
        user=user,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        old_value=str(old_value),
        new_value=str(new_value),
        ip_address=ip_address
    )
    
    logger.info(f"AUDIT LOG: {log_entry}")
    return log_entry
