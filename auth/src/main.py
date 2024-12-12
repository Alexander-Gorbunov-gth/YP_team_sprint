from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlmodel import SQLModel, create_engine

from src.db import redis
from src.db.postgres import create_database, purge_database
from src.api.v1.auth import auth_router
from src.api.v1.me import me_router
from src.api.v1.permission import perm_router
from src.api.v1.users import users_router
from src.services.cli_commands import typer_app

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: FastAPI):
    # redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    await purge_database()
    await create_database()
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


app.include_router(auth_router, prefix='/auth', tags=['auth'])
app.include_router(me_router, prefix='/me', tags=['me'])
app.include_router(users_router, prefix='/users', tags=['users'])
app.include_router(perm_router, prefix='/permissions', tags=['permissions'])

if __name__ == "__main__":
    typer_app()