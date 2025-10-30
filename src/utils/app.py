from fastapi import FastAPI

from typing import Optional

from services import Services


class App(FastAPI):
    services: Optional[Services]
