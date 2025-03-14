from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.api.v1.auth import auth_router
from src.api.v1.permission import perm_router
from src.api.v1.roles import roles_router
from src.api.v1.me import me_router
from src.core.config import settings
from src.core.exception_handlers import exception_handlers
from src.db import postgres, redis


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(host=settings.redis.redis_host, port=settings.redis.redis_port)
    postgres.engine = create_async_engine(settings.db.db_url, echo=True)
    postgres.async_session_maker = async_sessionmaker(bind=postgres.engine, expire_on_commit=False, class_=AsyncSession)
    await postgres.create_database()

    yield

    await postgres.purge_database()
    await redis.redis.close()


app = FastAPI(
    title=settings.service.project_name,
    docs_url="/api/openapi/",
    openapi_url="/api/openapi.json/",
    default_response_class=ORJSONResponse,
    exception_handlers=exception_handlers,
    lifespan=lifespan,
)


app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(me_router, prefix="/api/v1/me", tags=["me"])
app.include_router(roles_router, prefix="/api/v1/roles", tags=["roles"])
app.include_router(perm_router, prefix="/api/v1/permissions", tags=["permissions"])

if __name__ == "__main__":
    app()
