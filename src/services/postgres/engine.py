from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from core.config import postgres_config


async def postgres_startup_lifespan(app: FastAPI) -> None:
    postgres_engine: AsyncEngine | None = create_async_engine(
        url=postgres_config.database_url,
        echo=postgres_config.echo,
        pool_size=postgres_config.pool_size,
        max_overflow=postgres_config.max_overflow,
    )
    try:
        async with postgres_engine.begin() as _:
            print("Connected to PostgreSQL successfully!")
    except Exception as e:
        print(f"Failed to connect to PostgreSQL: {e}")

    app.state.postgres_engine = postgres_engine


async def postgres_shutdown_lifespan(app: FastAPI) -> None:
    print("Closing postgres connection...")
    postgres_engine: AsyncEngine | None = getattr(app.state, "postgres_engine", None)
    if postgres_engine:
        await postgres_engine.dispose()
    print("Postgres connection closed.")
