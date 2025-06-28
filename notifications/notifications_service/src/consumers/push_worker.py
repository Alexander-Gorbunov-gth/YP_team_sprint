import asyncio
import json
from aio_pika import connect_robust, IncomingMessage
from logging import getLogger
from httpx import AsyncClient

from src.infrastructure.messages import AbstractMessageMaker
from src.core.config import settings
from src.domain.tasks import MessageToSend
from src.domain.channels import ChannelTypes
from src.services.message_maker import get_message_maker
from src.services.email import get_email_sender
from src.infrastructure.repositories.messages_status import get_short_url_repository

logger = getLogger(__name__)


async def handle_message(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            logger.info(f"Получено сообщение Push: {data}")
            message = MessageToSend(**data)
            sender = get_email_sender(message)
            await sender.send()
            await get_short_url_repository().create(
                body=message.body,
                sent_to=message.user_uuid,
                sent_address=message.address,
                subject=message.subject
            )

        except Exception as e:
            logger.error(f"Ошибка обработки отправки Email: {e}")


async def start_push_consumer():
    connection = await connect_robust(settings.rabbit.rabbit_url)
    channel = await connection.channel()
    queue = await channel.declare_queue(settings.rabbit.push_queue_title, durable=True)
    await queue.consume(handle_message)
    logger.info("⏳ Консьюмер отправкипи Push запущен и слушает очередь")
    return connection
