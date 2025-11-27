import redis.asyncio as redis
from fastapi import HTTPException, status

from apps.user.schemas import (
    UserLoginIn,
    UserLoginOut,
    UserRefreshIn,
    UserRefreshOut,
)
from apps.user.models import TestDocument
from utils.jwt import jwt_handler


class UserController:
    @staticmethod
    async def login(
        body: UserLoginIn,
        redis_client: redis.Redis,
    ) -> UserLoginOut:
        if body.username != "test" or body.password != "test":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid username or password",
            )
        access, refresh = await jwt_handler.create_token_pair(
            payload=body.model_dump(),
            redis_client=redis_client,
        )
        t = TestDocument(name="test test")
        await t.insert()
        return UserLoginOut(
            access_token=access,
            refresh_token=refresh,
        )

    @staticmethod
    async def refresh(
        body: UserRefreshIn,
        redis_client: redis.Redis,
    ) -> UserRefreshOut:
        if not await jwt_handler.is_refresh_token_valid(
            refresh_token=body.refresh_token,
            redis_client=redis_client,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid refresh token",
            )
        await jwt_handler.revoke_refresh_token(
            refresh_token=body.refresh_token,
            redis_client=redis_client,
        )
        payload = await jwt_handler.decode(token=body.refresh_token)
        payload.pop("exp")
        payload.pop("iat")
        payload.pop("jti")
        payload.pop("type")
        access, refresh = await jwt_handler.create_token_pair(
            payload=payload,
            redis_client=redis_client,
        )
        return UserRefreshOut(
            access_token=access,
            refresh_token=refresh,
        )


user_controller = UserController()
