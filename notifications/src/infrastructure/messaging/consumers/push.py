import logging
from typing import Callable

from aio_pika import ExchangeType, RobustChannel, RobustConnection, RobustExchange, RobustQueue, connect_robust
from src.interfaces.connection import AbstractConnection

logger = logging.getLogger(__name__)


class PushConsumer(AbstractConnection):
    def __init__(self, connection_url: str, exchange_name: str, queue_name: str, handler: Callable) -> None:
        self.connection_url = connection_url
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.handler = handler

        self._connection: RobustConnection | None = None
        self._channel: RobustChannel | None = None
        self._exchange: RobustExchange | None = None
        self._queue: RobustQueue | None = None

    async def connect(self) -> None:
        logger.info("Инициализация потребителя push...")
        self._connection = await connect_robust(self.connection_url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            self.exchange_name, ExchangeType.X_DELAYED_MESSAGE, durable=True, arguments={"x-delayed-type": "direct"}
        )
        self._queue = await self._channel.declare_queue(self.queue_name, durable=True)
        await self._queue.bind(self._exchange, self.queue_name)
        logger.info(f"✅ Консьюмер успешно подключен")

    async def consume(self) -> None:
        async with self._queue.iterator() as it:
            async for message in it:
                logger.info(f"Получено сообщение: {message}")
                await self.handler(message)
                await message.ack()
                logger.info(f"✅ Сообщение успешно обработано")

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()
            logger.info(f"✅ Соединение с потребителем push закрыто")
