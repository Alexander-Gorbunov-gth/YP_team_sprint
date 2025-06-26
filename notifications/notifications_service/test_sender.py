import asyncio
import json
from aio_pika import connect_robust, Message, DeliveryMode

RABBITMQ_URL = "amqp://user:password@localhost:5672/"
QUEUE_NAME = "router_queue"

from src.domain.tasks import (
    IncomingTaskMessage,
)  # Импортируем модель IncomingTaskMessage


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
