import json
from logging import getLogger

from aio_pika import IncomingMessage, connect_robust
from src.core.config import settings
from src.domain.tasks import MessageToSend
from src.services.email import get_email_sender

logger = getLogger(__name__)


async def handle_message(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            logger.info(f"Получено сообщение Email: {data}")
            message = MessageToSend(**data)
            sender = get_email_sender(message)
            await sender.send()

        except Exception as e:
            logger.error(f"Ошибка обработки отправки Email: {e}")


async def start_email_consumer():
    connection = await connect_robust(settings.rabbit.connection_url)
    channel = await connection.channel()
    queue = await channel.declare_queue(settings.rabbit.email_queue_title, durable=True)
    await queue.consume(handle_message)
    logger.info("⏳ Консьюмер отправкипи Email запущен и слушает очередь")
    return connection
