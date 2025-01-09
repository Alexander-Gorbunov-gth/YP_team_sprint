from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from src.db import redis
from src.db.postgres import create_database, purge_database
from src.api.v1.auth import auth_router
from src.api.v1.me import me_router
from src.api.v1.permission import perm_router
from src.api.v1.users import users_router
from src.api.v1.roles import role_router
from src.services.cli_commands import typer_app
from src.core.exception_handlers import exception_handlers
from src.core.config import settings

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Инициализация соединения с Redis
    redis.redis = Redis.from_url(
        f"redis://{settings.redis.redis_host}:{settings.redis.redis_port}"
    )

    await purge_database()
    await create_database()

    yield

    await redis.redis.close()


# Создание приложения FastAPI
app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    exception_handlers=exception_handlers,
    lifespan=lifespan,
)

# Регистрация маршрутов
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(me_router, prefix="/me", tags=["me"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(role_router, prefix="/api/v1/roles", tags=["roles"])
app.include_router(perm_router, prefix="/api/v1/permissions", tags=["permissions"])

# Запуск приложения с помощью Typer (если требуется)
if __name__ == "__main__":
    typer_app()
