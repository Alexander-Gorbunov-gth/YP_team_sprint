import logging

from aio_pika.abc import HeadersType
from faststream.rabbit import ExchangeType, RabbitBroker, RabbitExchange

from src.interfaces.connection import AbstractConnection
from src.services.interfaces.producer import IProducer, PublishMessage

logger = logging.getLogger(__name__)


class RabbitMQProducer(IProducer, AbstractConnection):
    """Реализация абстрактного класса IProducer для отправки сообщений в RabbitMQ."""

    def __init__(self, connection_url: str, exchange_name: str) -> None:
        """
        Инициализирует RabbitMQProducer.
        :param connection_url: URL соединения с RabbitMQ
        :param exchange_name: Имя обменника
        """

        self.connection_url = connection_url
        self.exchange_name = exchange_name
        self._broker: RabbitBroker | None = None

    async def connect(self) -> None:
        """Устанавливает соединение с RabbitMQ и создает обменник."""

        logger.info("Инициализация продюсера RabbitMQ...")
        self._broker = RabbitBroker(
            self.connection_url,
            publisher_confirms=True,
        )

        exchange = RabbitExchange(
            name=self.exchange_name,
            type=ExchangeType.DIRECT,
            durable=True,
        )

        await self._broker.connect()
        await self._broker.declare_exchange(exchange)
        logger.info("✅ Соединение с продюсером RabbitMQ успешно установлено")

    async def close(self) -> None:
        """Закрывает соединение с RabbitMQ."""

        if self._broker is not None:
            await self._broker.stop()
            logger.info("✅ Соединение с продюсером RabbitMQ закрыто")

    async def publish(self, message: PublishMessage, routing_key: str, delay_ms: int | None = None) -> None:
        """
        Отправляет сообщение в RabbitMQ.
        :param message: Сообщение для отправки
        :param routing_key: Маршрут для отправки сообщения
        :param delay_ms: Задержка в миллисекундах
        """

        if self._broker is None:
            raise RuntimeError("Broker is not initialized")

        headers: HeadersType | None = None
        if delay_ms is not None:
            headers = {"x-delay": str(delay_ms)}

        await self._broker.publish(
            message=message.model_dump_json(),
            exchange=self.exchange_name,
            routing_key=routing_key,
            headers=headers,
            content_type="application/json",
            persist=True,
        )

        logger.info(
            "➡ Сообщение опубликовано в exchange '%s' → '%s' с задержкой %s мс.",
            self.exchange_name,
            routing_key,
            delay_ms,
        )

producer: RabbitMQProducer | None = None
