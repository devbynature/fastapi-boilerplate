from sqlmodel.ext.asyncio.session import AsyncSession

from typing import Optional

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from core.config import database_config


class PostgresService:
    def __init__(self):
        self._engine: Optional[AsyncEngine] = None

    async def create_engine(self) -> None:
        engine: AsyncEngine = create_async_engine(
            url=database_config.database_url,
            echo=database_config.echo,
            pool_size=database_config.pool_size,
            max_overflow=database_config.max_overflow,
        )
        self._engine = engine

    async def get_session(self) -> AsyncSession:
        session = sessionmaker(  # noqa
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with session() as session:
            yield session  # noqa

    async def get_engine(self) -> AsyncEngine:
        return self._engine
