import time
from typing import Any, Callable

class TTLCache:
    def __init__(self): self.data = {}
    def get(self, key):
        v = self.data.get(key)
        if not v: return None
        val, exp = v
        if exp and exp < time.time():
            self.data.pop(key, None); return None
        return val
    def set(self, key, val, ttl: int | None):
        exp = (time.time() + ttl) if ttl else None
        self.data[key] = (val, exp)
        
cache = TTLCache()

def cached(key_fn: Callable[..., str], ttl: int):
    def deco(fn):
        def wrap(*args, **kwargs):
            key = key_fn(*args, **kwargs)
            hit = cache.get(key)
            if hit is not None: return hit
            val = fn(*args, **kwargs)
            cache.set(key, val, ttl)
            return val
        return wrap
    return deco