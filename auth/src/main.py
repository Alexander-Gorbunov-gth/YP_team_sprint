from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlmodel import SQLModel, create_engine

from src.core.config import settings
from src.db import redis
from src.db.develop_db import develop_db_worker
from src.api.v1.auth import auth_router
from src.api.v1.me import me_router
from src.api.v1.permission import perm_router
from src.api.v1.users import users_router

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: FastAPI):
    # redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)

    yield

    # Закрытие соединений при завершении работы
    await redis.redis.close()


app = FastAPI(
    # title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

if settings.debug:
    develop_db_worker()

app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(me_router, prefix='/me', tags=['me'])
app.include_router(users_router, prefix='/users', tags=['users'])
app.include_router(perm_router, prefix='/permissions', tags=['permissions'])
