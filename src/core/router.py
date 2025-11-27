from fastapi import APIRouter, FastAPI

from apps.user.apis import user_router

main_router = APIRouter(
    prefix="/api/v1",
)


def initialize_routes(app: FastAPI):
    main_router.include_router(user_router)
    app.state

    app.include_router(main_router)
