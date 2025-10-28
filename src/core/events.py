from services.postgres.connection import engine


async def startup_event_handler() -> None:
    pass


async def shutdown_event_handler() -> None:
    # await engine.dispose()
    pass
