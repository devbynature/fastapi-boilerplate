import redis.asyncio as redis
from fastapi import APIRouter, status, Depends

from apps.user.controllers import user_controller
from apps.user.schemas import (
    UserLoginIn,
    UserLoginOut,
    UserRefreshIn,
    UserRefreshOut,
)
from services.redis.dependencies import get_redis

user_router = APIRouter(
    tags=["user"],
    prefix="/user",
)


@user_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    body: UserLoginIn,
    redis_client: redis.Redis = Depends(get_redis),
) -> UserLoginOut:
    return await user_controller.login(
        body=body,
        redis_client=redis_client,
    )


@user_router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh(
    body: UserRefreshIn,
    redis_client: redis.Redis = Depends(get_redis),
) -> UserRefreshOut:
    return await user_controller.refresh(
        body=body,
        redis_client=redis_client,
    )
