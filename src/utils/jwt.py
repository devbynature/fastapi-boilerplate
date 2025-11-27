import uuid
import redis.asyncio as redis
import jwt
from datetime import timedelta

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import app_config
from utils.ext import utc_now


class JWTHandler:
    security: HTTPBearer = HTTPBearer()
    secret_key: str = app_config.secret_key
    algorithm: str = "HS256"

    async def _encode(
        self,
        payload: dict,
        token_type: str,
        expires_in_minutes: int,
        jti: uuid.UUID,
    ) -> str:
        payload.update(
            {
                "jti": str(jti),
                "iat": utc_now(),
                "exp": utc_now() + timedelta(minutes=expires_in_minutes),
                "type": token_type,
            }
        )
        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    async def create_access_token(self, payload: dict) -> str:
        return await self._encode(
            payload=payload,
            token_type="access",
            expires_in_minutes=15,
            jti=uuid.uuid4(),
        )

    async def create_refresh_token(
        self, payload: dict, redis_client: redis.Redis
    ) -> str:
        refresh_expires_in_minutes = 131400  # 3 months
        jti = uuid.uuid4()
        refresh = await self._encode(
            payload=payload,
            token_type="refresh",
            expires_in_minutes=refresh_expires_in_minutes,
            jti=jti,
        )
        await redis_client.set(
            name=str(jti),
            value=refresh,
            ex=timedelta(minutes=refresh_expires_in_minutes).seconds,
        )
        return refresh

    async def create_token_pair(
        self, payload: dict, redis_client: redis.Redis
    ) -> tuple[str, str]:
        access = await self.create_access_token(payload)
        refresh = await self.create_refresh_token(payload, redis_client)
        return access, refresh

    async def revoke_refresh_token(
        self, refresh_token: str, redis_client: redis.Redis
    ) -> None:
        payload: dict = await self.decode(refresh_token)
        jti: str | None = payload.get("jti", None)
        if jti:
            await redis_client.delete(jti)

    async def is_refresh_token_valid(
        self, refresh_token: str, redis_client: redis.Redis
    ) -> bool:
        payload: dict = await self.decode(refresh_token)
        jti: str | None = payload.get("jti", None)
        if not jti:
            return False
        return refresh_token == await redis_client.get(jti)

    async def decode(self, token) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            return payload
        except jwt.exceptions.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

    async def auth_wrapper(
        self, auth: HTTPAuthorizationCredentials = Security(security)
    ) -> dict:
        try:
            payload = await self.decode(auth.credentials)
            if payload.get("type") != "access":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden",
                )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Signature has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        except KeyError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


jwt_handler = JWTHandler()
