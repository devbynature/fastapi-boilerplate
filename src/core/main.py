from contextlib import asynccontextmanager

from fastapi import FastAPI

from core import events
from core.router import initialize_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On Startup
    await events.startup_event_handler()

    yield

    # On Shutdown
    await events.shutdown_event_handler()


app = FastAPI(
    lifespan=lifespan,
)


initialize_routes(app=app)
