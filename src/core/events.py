from services.postgres.connection import engine
from utils.exceptions import PostgresConnectionErr


async def startup_event_handler() -> None:
    try:
        await engine.connect()
    except Exception:
        raise PostgresConnectionErr("postgres connection Failed")


async def shutdown_event_handler() -> None:
    await engine.dispose()
