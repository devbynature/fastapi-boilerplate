from utils.app import App
from utils.exceptions import PostgresConnectionErr, RedisConnectionErr
from services import Services


async def startup_event_handler(app: App) -> None:
    services = Services()
    app.services = services

    try:
        await app.services.postgres.create_engine()
    except Exception:
        raise PostgresConnectionErr("postgres connection failed")

    try:
        r = await app.services.redis.connect()
        await r.ping()
    except Exception:
        raise RedisConnectionErr("redis connection failed")


async def shutdown_event_handler(app: App) -> None:
    postgres = await app.services.postgres.get_engine()
    await postgres.dispose()

    redis = await app.services.redis.get_client()
    await redis.close()
