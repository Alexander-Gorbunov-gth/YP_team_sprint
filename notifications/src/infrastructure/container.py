import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.admin.auth import AdminAuth
from src.admin.config import add_views
from src.core.config import settings
from src.infrastructure.connections.db import AsyncDatabase
from src.infrastructure.connections.http import HttpClient
from src.infrastructure.messaging.producer import RabbitMQProducer
from src.interfaces.container import AbstractContainer

logger = logging.getLogger(__name__)


class AppContainer(AbstractContainer):
    _producer: RabbitMQProducer | None = None
    _db_session_factory: async_sessionmaker | None = None
    _http_client: AsyncDatabase | None = None
    _db_client: AsyncDatabase | None = None
    _admin: Admin | None = None

    @classmethod
    async def startup(self, app: FastAPI) -> None:
        """Запускает контейнер."""

        self._producer = RabbitMQProducer(settings.rabbit.connection_url, settings.rabbit.exchange_name)
        await self._producer.connect()

        self._http_client = HttpClient()
        await self._http_client.connect()

        self._db_client = AsyncDatabase(settings.db.connection_url)
        self._db_session_factory = await self._db_client.connect()

        self._admin = Admin(
            app=app,
            engine=self._db_client._engine,
            session_maker=self._db_session_factory,
            authentication_backend=AdminAuth(secret_key=settings.admin.secret_key),
        )
        await add_views(admin=self._admin)

    @classmethod
    async def shutdown(self) -> None:
        """Останавливает контейнер."""

        if self._producer is not None:
            await self._producer.close()

        if self._http_client is not None:
            await self._http_client.close()

        if self._db_client is not None:
            await self._db_client.close()

    @classmethod
    async def get_producer(self) -> RabbitMQProducer:
        if self._producer is None:
            raise RuntimeError("Продюсер не был запущен...")
        return self._producer

    @classmethod
    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        if self._db_session_factory is None:
            raise RuntimeError("Фабрика сессий не была запущена...")
        async with self._db_session_factory() as session:
            yield session

    @classmethod
    async def get_http_client(self) -> HttpClient:
        if self._http_client is None:
            raise RuntimeError("HTTP клиент не был запущен...")
        return self._http_client
