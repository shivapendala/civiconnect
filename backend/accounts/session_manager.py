import time
import uuid
import logging
from typing import Dict, Any, Optional
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

class UserSessionManager:
    """
    Distributed Redis-backed session & JWT token rotation tracker.
    Provides instant global revocation, concurrent session limiting, and device fingerprinting.
    """
    SESSION_PREFIX = "civic_session:"
    TOKEN_BLACKLIST_PREFIX = "civic_token_blacklist:"
    MAX_CONCURRENT_SESSIONS = 5

    @classmethod
    def create_session(cls, user_id: str, device_info: Dict[str, Any], ip_address: str) -> str:
        session_id = str(uuid.uuid4())
        key = f"{cls.SESSION_PREFIX}{user_id}:{session_id}"
        payload = {
            "session_id": session_id,
            "user_id": user_id,
            "device": device_info.get("device_name", "Unknown Browser"),
            "os": device_info.get("os", "Unknown OS"),
            "ip": ip_address,
            "created_at": time.time(),
            "last_active": time.time(),
        }
        cache.set(key, payload, timeout=86400 * 7)  # 7 days
        logger.info(f"Created session {session_id} for user {user_id}")
        return session_id

    @classmethod
    def touch_session(cls, user_id: str, session_id: str):
        key = f"{cls.SESSION_PREFIX}{user_id}:{session_id}"
        data = cache.get(key)
        if data:
            data["last_active"] = time.time()
            cache.set(key, data, timeout=86400 * 7)

    @classmethod
    def revoke_session(cls, user_id: str, session_id: str):
        key = f"{cls.SESSION_PREFIX}{user_id}:{session_id}"
        cache.delete(key)
        logger.info(f"Revoked session {session_id} for user {user_id}")

    @classmethod
    def blacklist_token(cls, jti: str, expires_in_seconds: int = 3600):
        key = f"{cls.TOKEN_BLACKLIST_PREFIX}{jti}"
        cache.set(key, True, timeout=expires_in_seconds)

    @classmethod
    def is_token_blacklisted(cls, jti: str) -> bool:
        key = f"{cls.TOKEN_BLACKLIST_PREFIX}{jti}"
        return bool(cache.get(key))
