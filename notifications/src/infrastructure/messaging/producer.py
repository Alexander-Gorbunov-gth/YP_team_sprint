import json
import logging
from typing import Any

from aio_pika import (
    DeliveryMode,
    ExchangeType,
    Message,
    RobustChannel,
    RobustConnection,
    RobustExchange,
    connect_robust,
)
from src.interfaces.connection import AbstractConnection
from src.services.interfaces.messaging.producer import AbstractProducer

logger = logging.getLogger(__name__)


class RabbitMQProducer(AbstractProducer, AbstractConnection):
    """Реализация абстрактного класса AbstractProducer для отправки сообщений в RabbitMQ"""

    def __init__(self, connection_url: str, exchange_name: str) -> None:
        """
        Инициализирует RabbitMQProducer.
        :param connection_url: URL соединения с RabbitMQ
        :param exchange_name: Имя обменника
        """

        self.connection_url = connection_url
        self.exchange_name = exchange_name

        self._connection: RobustConnection | None = None
        self._channel: RobustChannel | None = None
        self._exchange: RobustExchange | None = None

    async def connect(self) -> None:
        """Устанавливает соединение с RabbitMQ и создает обменник."""
        logger.info("Инициализация продюсера RabbitMQ...")
        self._connection = await connect_robust(self.connection_url)
        self._channel = await self._connection.channel(publisher_confirms=True)
        self._exchange = await self._channel.declare_exchange(
            self.exchange_name,
            ExchangeType.X_DELAYED_MESSAGE,
            durable=True,
            arguments={"x-delayed-type": "direct"},
        )
        logger.info("✅ Соединение с продюсером RabbitMQ успешно установлено")

    async def close(self) -> None:
        """Закрывает соединение с RabbitMQ."""

        if self._connection is not None:
            await self._connection.close()
            logger.info(f"✅ Соединение с продюсером RabbitMQ закрыто")

    async def send(
        self, message: dict[str, Any], routing_key: str, delay_ms: int | None = None
    ) -> None:
        """
        Отправляет сообщение в RabbitMQ.
        :param message: Сообщение для отправки
        :param routing_key: Маршрут для отправки сообщения
        :param delay_ms: Задержка в миллисекундах
        """

        message = Message(
            body=json.dumps(message).encode(),
            headers={"x-delay": delay_ms} if delay_ms else None,
        )
        await self._exchange.publish(message, routing_key=routing_key)
        logger.info(
            "➡ Сообщение опубликовано в exchange '%s' → '%s' с задержкой %s мс.",
            self.exchange_name,
            routing_key,
            delay_ms,
        )
