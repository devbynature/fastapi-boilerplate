from typing import AsyncGenerator
from fastapi import HTTPException
import redis.asyncio as redis
from services.redis.client import redis_client


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """
    Dependency to inject the Redis client into route handlers.
    """
    if redis_client is None:
        raise HTTPException(status_code=500, detail="Redis client not initialized")

    yield redis_client
