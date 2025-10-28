from fastapi import APIRouter, status

from src.apps.ping.controllers import ping_controller

ping_router = APIRouter(
    tags=["ping"],
)


@ping_router.get(
    "/ping",
    status_code=status.HTTP_200_OK,
)
def ping():
    return ping_controller.ping()
