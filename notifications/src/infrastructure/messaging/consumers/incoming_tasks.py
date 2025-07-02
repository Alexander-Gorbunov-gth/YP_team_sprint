import logging
from typing import Callable

from aio_pika import (
    ExchangeType,
    RobustChannel,
    RobustConnection,
    RobustExchange,
    RobustQueue,
    connect_robust,
)
from src.interfaces.connection import AbstractConnection

logger = logging.getLogger(__name__)


class IncomingTaskConsumer(AbstractConnection):
    def __init__(self, connection_url: str, queue_name: str, handler: Callable) -> None:
        self.connection_url = connection_url
        self.queue_name = queue_name
        self.handler = handler

        self._connection: RobustConnection | None = None
        self._channel: RobustChannel | None = None
        self._queue: RobustQueue | None = None

        self._title = "Incoming Task Consumer"

    async def connect(self) -> None:
        logger.info(f"Инициализация потребителя {self._title}...")
        self._connection = await connect_robust(self.connection_url)
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(self.queue_name, durable=True)
        logger.info(f"✅ {self._title} успешно подключен")

    async def consume(self) -> None:
        await self._queue.consume(self.handler)
        logger.info(f"⏳ {self._title} запущен и слушает очередь {self.queue_name}")

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()
            logger.info(f"✅ Соединение с {self._title} закрыто")
