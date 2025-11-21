from fastapi import FastAPI
from services.redis.client import redis_startup_lifespan, redis_shutdown_lifespan
from services.postgres.engine import (
    postgres_startup_lifespan,
    postgres_shutdown_lifespan,
)
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await postgres_startup_lifespan(app)
    await redis_startup_lifespan(app)

    yield

    await redis_shutdown_lifespan(app)
    await postgres_shutdown_lifespan(app)
