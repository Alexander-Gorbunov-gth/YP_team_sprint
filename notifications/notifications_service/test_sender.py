import asyncio
import json
from aio_pika import connect_robust, Message, DeliveryMode

RABBITMQ_URL = "amqp://user:password@localhost:5672/"
QUEUE_NAME = "router_queue"

from src.domain.tasks import TaskMessage  # Импортируем модель TaskMessage


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
    message = TaskMessage(
        event_type="send_notification",
        channels=["email", "push"],
        for_all_users=False,
        user_uuid="123e4567-e89b-12d3-a456-426614174000",
        params={"key1": "value1", "key2": "value2"},
        send_in_local_time=False,
        send_at=None,
    )
    message_for_send = message.model_dump(mode="json", exclude_none=True)
    print(f"Отправляемое сообщение: {message_for_send}")
    asyncio.run(send_message(message_for_send))
