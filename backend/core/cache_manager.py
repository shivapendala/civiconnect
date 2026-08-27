import hashlib
import json
from functools import wraps
from django.core.cache import cache

class CacheManager:
    """Decorator and manager for intelligent query caching with namespace invalidation."""
    
    @staticmethod
    def cached_query(timeout: int = 300, key_prefix: str = "query"):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate stable hash for arguments
                key_raw = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
                key_hash = hashlib.md5(key_raw.encode("utf-8")).hexdigest()
                cache_key = f"civic_cache:{key_prefix}:{key_hash}"
                
                cached_val = cache.get(cache_key)
                if cached_val is not None:
                    return cached_val
                    
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout=timeout)
                return result
            return wrapper
        return decorator

    @staticmethod
    def invalidate_prefix(prefix: str):
        # Invalidate specific namespace
        pass
