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
from src.infrastructure.messaging.consumers.incoming_tasks import IncomingTaskConsumer
from src.services.handlers.incoming_tasks import incoming_handle_message
from src.infrastructure.messaging.consumers.send_messages import SendMessageConsumer
from src.domain.channels import ChannelTypes
from src.db.postgres import create_database

logger = logging.getLogger(__name__)


class AppContainer(AbstractContainer):
    _producer: RabbitMQProducer | None = None
    _db_session_factory: async_sessionmaker | None = None
    _http_client: AsyncDatabase | None = None
    _db_client: AsyncDatabase | None = None
    _admin: Admin | None = None
    _incoming_consumer: IncomingTaskConsumer | None = None

    async def _init_rabbit(self) -> None:
        """Инициализирует соединения с RabbitMQ."""

        self._producer = RabbitMQProducer(
            settings.rabbit.connection_url, settings.rabbit.exchange_name
        )
        await self._producer.connect()

        self._incoming_consumer = IncomingTaskConsumer(
            connection_url=settings.rabbit.connection_url,
            queue_name=settings.rabbit.router_queue_title,
            handler=incoming_handle_message,
        )

        await self._incoming_consumer.connect()
        await self._incoming_consumer.consume()

        for channel in ChannelTypes:
            setattr(
                self,
                f"_{channel.value}_consumer",
                SendMessageConsumer(
                    connection_url=settings.rabbit.connection_url,
                    channel_name=channel.value,
                ),
            )
            consumer = getattr(self, f"_{channel.value}_consumer")
            if consumer:
                await consumer.connect()
                await consumer.consume()

    @classmethod
    async def startup(self, app: FastAPI) -> None:
        """Запускает контейнер."""

        logger.info("Инициализация контейнера приложения...")

        self._http_client = HttpClient()
        await self._http_client.connect()

        self._db_client = AsyncDatabase(settings.db.connection_url)
        self._db_session_factory = await self._db_client.connect()
        await create_database(self._db_client._engine)

        self._admin = Admin(
            app=app,
            engine=self._db_client._engine,
            session_maker=self._db_session_factory,
            authentication_backend=AdminAuth(secret_key=settings.admin.secret_key),
        )
        await add_views(admin=self._admin)

        await self._init_rabbit(self)

    @classmethod
    async def shutdown(self) -> None:
        """Останавливает контейнер."""

        if self._producer is not None:
            await self._producer.close()

        if self._http_client is not None:
            await self._http_client.close()

        if self._db_client is not None:
            await self._db_client.close()

        for channel in ChannelTypes:
            consumer = getattr(self, f"_{channel.value}_consumer")
            if consumer is not None:
                await consumer.close()

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
