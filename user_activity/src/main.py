from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings
from src.infrastructure import db
from src.infrastructure.models import BookmarksModel, LikesModel, ReviewsModel


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    db.mongo_client = AsyncIOMotorClient(settings.mongo.connection_url)
    await init_beanie(
        database=db.mongo_client[settings.mongo.db_name],
        document_models=[LikesModel, BookmarksModel, ReviewsModel],
    )

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.proect.title,
        description=settings.proect.decription,
        debug=settings.proect.debug,
        lifespan=lifespan,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
    )
    return app


app = create_app()


if __name__ == "__main__":
    app()
