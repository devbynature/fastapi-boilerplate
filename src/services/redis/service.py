import redis.asyncio as redis

from typing import Optional

from core.config import redis_config


class RedisService:
    def __init__(self):
        self._client: Optional[redis.Redis] = None

    async def connect(self) -> redis.Redis:
        self._client = redis.from_url(redis_config.redis_url)
        return self._client

    async def get_client(self) -> redis.Redis:
        return self._client


redis_service = RedisService()
