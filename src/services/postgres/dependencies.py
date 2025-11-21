from typing import AsyncGenerator
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from services.postgres.engine import postgres_engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if postgres_engine is None:
        raise HTTPException(status_code=500, detail="Redis client not initialized")
    session = sessionmaker(  # noqa
        postgres_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session() as session:
        yield session
