import time
from typing import Tuple
from django.core.cache import cache

class DistributedRateLimiter:
    """Sliding window token bucket rate limiter backed by Redis."""
    
    @classmethod
    def is_rate_limited(cls, key: str, max_requests: int = 100, window_seconds: int = 60) -> Tuple[bool, int]:
        cache_key = f"civic_ratelimit:{key}"
        now = time.time()
        
        pipe = cache.get(cache_key) or []
        # Filter timestamps within active sliding window
        valid_timestamps = [ts for ts in pipe if (now - ts) < window_seconds]
        
        if len(valid_timestamps) >= max_requests:
            remaining = 0
            return True, remaining
            
        valid_timestamps.append(now)
        cache.set(cache_key, valid_timestamps, timeout=window_seconds)
        remaining = max_requests - len(valid_timestamps)
        return False, remaining
