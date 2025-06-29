# src/infra/rabbit/producer.py
import json
from logging import getLogger
from typing import Optional

from aio_pika import (
    ExchangeType,
    Message,
    RobustChannel,
    RobustConnection,
    RobustExchange,
    connect_robust,
)

logger = getLogger(__name__)


class RabbitMQPublisher:
    def __init__(self, url: str, exchange_name: str = "notifications"):
        self._url = url
        self._exchange_name = exchange_name
        self._connection: Optional[RobustConnection] = None
        self._channel: Optional[RobustChannel] = None
        self._exchange: Optional[RobustExchange] = None

    async def connect(self):
        self._connection = await connect_robust(self._url)
        self._channel = await self._connection.channel()

        self._exchange = await self._channel.declare_exchange(
            name=self._exchange_name,
            type=ExchangeType.X_DELAYED_MESSAGE,
            durable=True,
            arguments={"x-delayed-type": "direct"},
        )

        logger.info(f"✅ Exchange '{self._exchange_name}' создан с типом 'x-delayed-message'")
        logger.info("✅ Подключение к RabbitMQ установлено (Publisher)")

    async def close(self):
        if self._connection:
            await self._connection.close()
            logger.info("❌ Подключение к RabbitMQ закрыто (Publisher)")

    async def publish(
        self,
        routing_key: str,
        payload: dict,
        delay_ms: Optional[int] = None,
    ):
        if not self._exchange:
            raise RuntimeError("Exchange не инициализирован")

        message = Message(
            body=json.dumps(payload).encode(),
            content_type="application/json",
            headers={"x-delay": delay_ms} if delay_ms else None,
        )

        await self._exchange.publish(message, routing_key=routing_key)
        logger.info(
            f"➡ Сообщение опубликовано в exchange '{self._exchange_name}' → '{routing_key}' с задержкой {delay_ms or 0} мс: {payload}"
        )
