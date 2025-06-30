import json
from logging import getLogger

from aio_pika import IncomingMessage, connect_robust, Message, DeliveryMode
from src.core.config import settings
from src.domain.tasks import MessageToSend
from src.infrastructure.repositories.messages_status import get_short_url_repository
from src.services.email import get_email_sender

logger = getLogger(__name__)


async def handle_message(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            logger.info(f"Получено сообщение Email: {data}")
            message_model = MessageToSend(**data)
            sender = get_email_sender(message_model)
            result = await sender.send()

            if not result:
                logger.error(
                    f"Не удалось отправить Email: {message_model.address}, {message_model.body}"
                )

                # Увеличиваем счётчик попыток
                data["retry_count"] = data.get("retry_count", 0) + 1

                if data["retry_count"] < settings.rabbit.max_retry_count:
                    delay_ms = 10000 * data["retry_count"]  # 10 сек * попытка

                    # Публикуем повторно в DLX с задержкой
                    dlx_exchange = await message.channel.get_exchange(
                        "dead_letter_exchange", ensure=True
                    )

                    await dlx_exchange.publish(
                        Message(
                            body=json.dumps(data).encode(),
                            delivery_mode=DeliveryMode.PERSISTENT,
                            headers={"x-delay": delay_ms},
                        ),
                        routing_key=f"{settings.rabbit.email_queue_title}_dlq",
                    )
                    await message.ack()
                else:
                    logger.error(
                        f"Максимальное количество попыток отправки Email достигнуто: {message_model.address}"
                    )
                    await message.nack(requeue=False)
                return

            await get_short_url_repository().create(
                body=message.body,
                sent_to=message.user_uuid,
                sent_address=message.address,
                subject=message.subject,
            )

        except Exception as e:
            logger.error(f"Ошибка обработки отправки Email: {e}")


async def start_email_consumer():
    connection = await connect_robust(settings.rabbit.connection_url)
    channel = await connection.channel()

    dead_letter_exchange = await channel.declare_exchange(
        "dead_letter_exch",
        type="x-delayed-message",
        durable=True,
        arguments={"x-delayed-type": "direct"},
    )

    dlq_queue = await channel.declare_queue(
        f"{settings.rabbit.email_queue_title}_dlq", durable=True
    )
    await dlq_queue.bind(
        exchange=dead_letter_exchange,
        routing_key=f"{settings.rabbit.email_queue_title}_dlq",
    )
    main_queue = await channel.declare_queue(
        settings.rabbit.email_queue_title,
        durable=True,
        arguments={
            "x-dead-letter-exchange": "dead_letter_exchange",
            "x-dead-letter-routing-key": f"{settings.rabbit.email_queue_title}_dlq",
        },
    )
    await main_queue.consume(handle_message)
    logger.info("⏳ Консьюмер отправки Email запущен и слушает очередь")
    return connection
