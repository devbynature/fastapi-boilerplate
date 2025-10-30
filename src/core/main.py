from contextlib import asynccontextmanager

from utils.app import App
from core import events
from core.router import initialize_routes


@asynccontextmanager
async def lifespan(app: App):
    # On Startup
    await events.startup_event_handler(app=app)

    yield

    # On Shutdown
    await events.shutdown_event_handler(app=app)


app = App(
    lifespan=lifespan,
)


initialize_routes(app=app)
