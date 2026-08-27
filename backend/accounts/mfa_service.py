import base64
import hmac
import hashlib
import struct
import time
import secrets
import logging
from typing import Tuple, List, Optional
from django.conf import settings
from django.utils import timezone
from .models import User

logger = logging.getLogger(__name__)

class MFAService:
    """
    Multi-Factor Authentication (MFA / 2FA) Service implementing Time-based One-Time Password (TOTP)
    algorithm conforming to RFC 6238 and HMAC-based One-Time Password (HOTP) RFC 4226.
    """
    DIGITS = 6
    TIME_STEP_SECONDS = 30

    @classmethod
    def generate_secret(cls) -> str:
        """Generates cryptographically random base32 encoded secret key."""
        random_bytes = secrets.token_bytes(20)
        return base64.b32encode(random_bytes).decode("utf-8")

    @classmethod
    def get_totp_token(cls, secret: str, time_step: Optional[int] = None) -> str:
        """Calculates 6-digit TOTP token for given secret at current time step."""
        if time_step is None:
            time_step = int(time.time() // cls.TIME_STEP_SECONDS)
            
        key = base64.b32decode(secret, casefold=True)
        msg = struct.pack(">Q", time_step)
        h = hmac.new(key, msg, hashlib.sha1).digest()
        
        offset = h[19] & 0x0F
        code = (
            (h[offset] & 0x7F) << 24
            | (h[offset + 1] & 0xFF) << 16
            | (h[offset + 2] & 0xFF) << 8
            | (h[offset + 3] & 0xFF)
        )
        token = str(code % (10 ** cls.DIGITS)).zfill(cls.DIGITS)
        return token

    @classmethod
    def verify_token(cls, secret: str, token: str, window: int = 1) -> bool:
        """Verifies provided token against secret, allowing for clock skew window."""
        current_step = int(time.time() // cls.TIME_STEP_SECONDS)
        for offset in range(-window, window + 1):
            valid_token = cls.get_totp_token(secret, current_step + offset)
            if hmac.compare_digest(valid_token, token):
                return True
        return False

    @classmethod
    def generate_backup_codes(cls, count: int = 8) -> List[str]:
        """Generates emergency backup recovery codes."""
        codes = []
        for _ in range(count):
            code = f"{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}"
            codes.append(code)
        return codes

    @classmethod
    def enable_mfa_for_user(cls, user: User) -> Tuple[str, List[str], str]:
        """Enables 2FA for staff or administrator account."""
        secret = cls.generate_secret()
        backup_codes = cls.generate_backup_codes()
        user.mfa_secret = secret
        user.is_mfa_enabled = True
        user.save(update_fields=["mfa_secret", "is_mfa_enabled"])
        
        totp_uri = f"otpauth://totp/CivicConnect:{user.email}?secret={secret}&issuer=CivicConnect"
        logger.info(f"MFA enabled for user {user.email}")
        return secret, backup_codes, totp_uri
