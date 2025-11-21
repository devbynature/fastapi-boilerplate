from fastapi import FastAPI
from core.lifespan import lifespan
from core.router import initialize_routes

app = FastAPI(
    lifespan=lifespan,
)


initialize_routes(app=app)
