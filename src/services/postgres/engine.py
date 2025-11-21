from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from core.config import database_config

postgres_engine: AsyncEngine | None = None


async def postgres_startup_lifespan(app: FastAPI) -> None:
    global postgres_engine

    postgres_engine = create_async_engine(
        url=database_config.database_url,
        echo=database_config.echo,
        pool_size=database_config.pool_size,
        max_overflow=database_config.max_overflow,
    )
    try:
        async with postgres_engine.begin() as _:
            print("Connected to PostgreSQL successfully!")
    except Exception as e:
        print(f"Failed to connect to PostgreSQL: {e}")


async def postgres_shutdown_lifespan(app: FastAPI) -> None:
    print("Closing postgres connection...")
    if postgres_engine:
        await postgres_engine.dispose()
    print("Postgres connection closed.")
