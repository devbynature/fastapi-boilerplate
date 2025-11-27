from fastapi import FastAPI
import redis.asyncio as redis
from core.config import redis_config


async def redis_startup_lifespan(app: FastAPI) -> None:
    redis_client = redis.from_url(
        redis_config.redis_url,
        encoding="utf-8",
        decode_responses=redis_config.decode_responses,
        max_connections=redis_config.max_connections,
    )

    try:
        await redis_client.ping()
        print("Connected to Redis successfully!")
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")

    app.state.redis_client = redis_client


async def redis_shutdown_lifespan(app: FastAPI) -> None:
    print("Closing Redis connection...")
    redis_client: redis.Redis | None = getattr(app.state, "redis", None)
    if redis_client:
        await redis_client.close()
    print("Redis connection closed.")
