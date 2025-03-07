from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.db import redis
from src.db import postgres
from src.api.v1.auth import auth_router
from temp.cli_commands import typer_app
from src.core.exception_handlers import exception_handlers
from src.core.config import settings

from contextlib import asynccontextmanager


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
    # title=settings.project_name,
    docs_url="/api/openapi/",
    openapi_url="/api/openapi.json/",
    default_response_class=ORJSONResponse,
    exception_handlers=exception_handlers,
    lifespan=lifespan,
)


app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
# app.include_router(me_router, prefix="/me", tags=["me"])
# app.include_router(users_router, prefix="/users", tags=["users"])
# app.include_router(perm_router, prefix="/permissions", tags=["permissions"])

if __name__ == "__main__":
    typer_app()
