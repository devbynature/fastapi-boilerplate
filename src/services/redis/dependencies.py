from typing import AsyncGenerator
from fastapi import HTTPException, Request
import redis.asyncio as redis


async def get_redis(request: Request) -> AsyncGenerator[redis.Redis, None]:
    """
    Dependency to inject the Redis client into route handlers.
    """
    redis_client: redis.Redis | None = getattr(request.app.state, "redis_client", None)
    if redis_client is None:
        raise HTTPException(status_code=500, detail="Redis client not initialized")

    yield redis_client
