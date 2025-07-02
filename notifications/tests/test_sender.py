import asyncio
import json
from datetime import datetime
from typing import Dict, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# from src.domain.tasks import (  # Импортируем модель IncomingTaskMessage
#     IncomingTaskMessage,
# )

from aio_pika import DeliveryMode, Message, connect_robust

RABBITMQ_URL = "amqp://u:p@localhost:5672/"
QUEUE_NAME = "router_queue"

from enum import Enum
from typing import Literal


class ChannelTypes(str, Enum):
    EMAIL = "email"
    PUSH = "push"


ChannelLiteral = Literal[ChannelTypes.EMAIL, ChannelTypes.PUSH]


class IncomingTaskMessage(BaseModel):

    event_type: str = Field(
        ...,
        description="Тип события, например 'send_notification'",
    )
    channels: list[ChannelLiteral] = Field(
        ...,
        description="Список каналов, допустимые значения: 'email', 'push'",
    )
    for_all_users: bool = Field(
        False,
        description="Флаг, указывающий, что событие для всех пользователей",
    )
    user_params: Dict[UUID, Dict[str, str]] | None = Field(
        None,
        description="Данные клиентов для отправки",
        example={"user_uuid": {"key1": "value1", "key2": "value2"}},
    )
    send_in_local_time: bool = Field(
        False,
        description="Флаг, указывающий, что время отправки события в локальном времени пользователя",
    )
    send_at: datetime | None = Field(
        None,
        description="Время отправки события. Если None, то событие отправляется немедленно",
        example="2023-10-01T12:00:00Z",
    )


async def send_message(payload: dict):
    # Подключение к RabbitMQ
    connection = await connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue(QUEUE_NAME, durable=True)

        # Сериализуем данные и создаём сообщение
        body = json.dumps(payload).encode()
        message = Message(
            body,
            content_type="application/json",
            delivery_mode=DeliveryMode.PERSISTENT,  # сохраняется при перезапуске брокера
        )

        # Публикуем в очередь
        await channel.default_exchange.publish(
            message,
            routing_key=QUEUE_NAME,
        )
        print(f"✅ Отправлено: {payload}")


if __name__ == "__main__":
    message = IncomingTaskMessage(
        event_type="send_notification",
        channels=["email", "push"],
        for_all_users=False,
        send_in_local_time=False,
        send_at="2024-06-27T12:00:00Z",
        user_params={
            "123e4567-e89b-12d3-a456-426614174000": {
                "param1": "value1",
                "param2": "value2",
            },
            "123e4567-e89b-12d3-a456-426614174001": {
                "param1": "value3",
                "param2": "value4",
            },
            "123e4567-e89b-12d3-a456-426614174002": {
                "param1": "value3",
                "param2": "value4",
            },
        },
    )
    message_for_send = message.model_dump(mode="json", exclude_none=True)
    print(f"Отправляемое сообщение: {message_for_send}")
    asyncio.run(send_message(message_for_send))
