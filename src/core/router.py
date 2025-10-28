from fastapi import FastAPI, APIRouter

from apps.ping.apis import ping_router

main_router = APIRouter()


def initialize_routes(app: FastAPI):
    app.include_router(main_router)
    app.include_router(ping_router)
