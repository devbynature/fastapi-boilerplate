from fastapi import APIRouter

from utils.app import App
from apps.ping.apis import ping_router

main_router = APIRouter()


def initialize_routes(app: App):
    app.include_router(main_router)
    app.include_router(ping_router)
