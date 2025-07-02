import importlib
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
from src.core.config import settings
from src.interfaces.connection import AbstractConnection

logger = logging.getLogger(__name__)


class SendMessageConsumer(AbstractConnection):
    def __init__(self, connection_url: str, channel_name: str) -> None:
        self.connection_url = connection_url
        self.channel_name = channel_name
        self.main_queue_name = f"{channel_name}_message_queue"
        self.dlq_queue_name = f"{channel_name}_dlq"
        self.exchange_name = settings.rabbit.exchange_name

        self.handler = self._get_handler()

        self._connection: RobustConnection | None = None
        self._channel: RobustChannel | None = None
        self._queue: RobustQueue | None = None
        self._dlq_queue: RobustQueue | None = None
        self._exchange: RobustExchange | None = None

        self._title = f"{channel_name} send consumer"

    def _get_handler(self) -> Callable:
        """
        Dynamically import the handler function based on the channel name.
        """
        module_path = f"src.services.handlers.{self.channel_name}"
        module = importlib.import_module(module_path)
        try:
            return getattr(module, f"{self.channel_name}_handle_message")
        except AttributeError as e:
            logger.error(f"Handler for {self.channel_name} not found: {e}")
            raise e

    async def connect(self) -> None:
        logger.info(f"Инициализация потребителя {self._title}...")
        self._connection = await connect_robust(self.connection_url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            self.exchange_name,
            ExchangeType.X_DELAYED_MESSAGE,
            durable=True,
        )
        self._dlq_queue = await self._channel.declare_queue(
            self.dlq_queue_name,
            durable=True,
            arguments={
                "x-message-ttl": settings.rabbit.dlq_ttl,
                "x-dead-letter-exchange": self.exchange_name,
                "x-dead-letter-routing-key": self.main_queue_name,
            },
        )
        self._queue = await self._channel.declare_queue(
            self.main_queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": self.exchange_name,
                "x-dead-letter-routing-key": self.dlq_queue_name,
            },
        )

        await self._dlq_queue.bind(self._exchange, routing_key=self.dlq_queue_name)
        await self._queue.bind(self._exchange, routing_key=self.main_queue_name)

    async def consume(self) -> None:
        await self._queue.consume(self.handler)
        logger.info(f"⏳ {self._title} запущен и слушает очередь {self.main_queue_name}")

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()
            logger.info(f"✅ Соединение с {self._title} закрыто")


async def start_email_consumer():
    connection = await connect_robust(settings.rabbit.connection_url)
    channel = await connection.channel()

    main_exchange = await channel.declare_exchange("email_exchange", durable=True, type="direct")
    dlq_queue_name = "email_dlq"
    dlq_queue = await channel.declare_queue(
        dlq_queue_name,
        durable=True,
        arguments={
            "x-message-ttl": settings.rabbit.dlq_ttl,
            "x-dead-letter-exchange": "email_exchange",
            "x-dead-letter-routing-key": settings.rabbit.email_queue_title,
        },
    )
    await dlq_queue.bind(main_exchange, routing_key=dlq_queue_name)

    main_queue = await channel.declare_queue(
        settings.rabbit.email_queue_title,
        durable=True,
        arguments={
            "x-dead-letter-exchange": "email_exchange",
            "x-dead-letter-routing-key": dlq_queue_name,
        },
    )
    await main_queue.bind(exchange=main_exchange, routing_key=settings.rabbit.email_queue_title)
    await main_queue.consume(handle_message, no_ack=False)
    logger.info("⏳ Консьюмер отправки Email запущен и слушает очередь")
    return connection
