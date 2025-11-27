from beanie import init_beanie
from pymongo import AsyncMongoClient
from fastapi import FastAPI

from core.config import mongo_config
from apps import document_models, TestDocument

mongo_client: AsyncMongoClient | None = None


async def mongo_startup_lifespan(app: FastAPI) -> None:
    global mongo_client

    mongo_client = AsyncMongoClient(
        mongo_config.mongo_url,
    )

    try:
        await init_beanie(
            database=mongo_client.db_name,
            document_models=document_models,
        )
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


async def mongo_shutdown_lifespan(app: FastAPI) -> None:
    print("Closing mongo connection.")
    if mongo_client:
        await mongo_client.close()
    print("Mongo connection closed.")
