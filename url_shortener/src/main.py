from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.api.router import router as api_router
from src.api.router import original_router as original_router
from src.core import http_client
from src.core.config import settings
from src.core.exception_handlers import exception_handlers
from src.db import postgres, redis


@asynccontextmanager
async def lifespan(_: FastAPI):
    http_client.http_client = AsyncClient()
    redis.redis = Redis(
        host=settings.redis.redis_host,
        port=settings.redis.redis_port
    )
    postgres.engine = create_async_engine(settings.db.db_url)
    postgres.async_session_maker = async_sessionmaker(
        bind=postgres.engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    yield

    await http_client.http_client.aclose()
    await redis.redis.close()
    await postgres.engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.service.project_name,
        docs_url="/api/openapi/",
        openapi_url="/api/openapi.json/",
        default_response_class=ORJSONResponse,
        exception_handlers=exception_handlers,
        lifespan=lifespan,
    )

    app.include_router(api_router)
    app.include_router(original_router)
    return app


app = create_app()


if __name__ == "__main__":
    app()
