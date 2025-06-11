from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from src.api.router import router as api_router
from src.core.config import settings
from src.infrastructure import db
from src.infrastructure.clients import http
from src.infrastructure.models import BookmarkModel, LikeModel, ReviewModel


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    db.mongo_client = AsyncIOMotorClient(settings.mongo.connection_url)
    await init_beanie(
        database=db.mongo_client[settings.mongo.db_name],
        document_models=[LikeModel, BookmarkModel, ReviewModel],
    )
    http.httpx_client = AsyncClient(timeout=5.0)

    yield

    await http.httpx_client.aclose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.proect.title,
        description=settings.proect.decription,
        debug=settings.proect.debug,
        lifespan=lifespan,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        response_class=ORJSONResponse,
    )
    app.include_router(api_router)
    return app


app = create_app()


if __name__ == "__main__":
    app()
