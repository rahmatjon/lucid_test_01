from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from typing import Dict, Any

class CacheService:
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}

    def get_cached_response(self, user_id: str, endpoint: str):
        cache_key = f"{user_id}_{endpoint}"
        cached_data = self.cache.get(cache_key)
        if cached_data and datetime.now() < cached_data["expires_at"]:
            return cached_data["data"]
        return None

    def set_cached_response(self, user_id: str, endpoint: str, data: Any, ttl: int = 300):
        cache_key = f"{user_id}_{endpoint}"
        self.cache[cache_key] = {
            "data": data,
            "expires_at": datetime.now() + timedelta(seconds=ttl)
        }

cache_service = CacheService()