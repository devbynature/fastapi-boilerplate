from typing import AsyncGenerator
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    postgres_engine: AsyncEngine | None = getattr(
        request.app.state, "postgres_engine", None
    )
    if not postgres_engine:
        raise HTTPException(status_code=500, detail="postgres client not initialized")
    session = sessionmaker(  # noqa
        postgres_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session() as session:
        yield session
