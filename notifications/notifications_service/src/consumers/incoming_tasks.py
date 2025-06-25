import asyncio
import json
from aio_pika import connect_robust, IncomingMessage
from logging import getLogger

from src.core.config import settings
from src.domain.tasks import TaskMessage  # Импортируем модель TaskMessage
from src.domain.channels import ChannelTypes
from src.services.email import get_email_message_maker

logger = getLogger(__name__)


async def handle_message(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            logger.info(f"Получено сообщение: {data}")
            task_message = TaskMessage(**data)
            for channel in task_message.channels:
                if channel == ChannelTypes.EMAIL:
                    logger.info(f"Обработка email для: {task_message.user_uuid}")
                    email_maker = get_email_message_maker()
                    await email_maker.run(task_message)
                elif channel == ChannelTypes.PUSH:
                    # Здесь должна быть логика обработки push-уведомлений
                    logger.info(f"Обработка push для: {task_message.user_uuid}")
                else:
                    logger.warning(f"Неизвестный канал: {channel}")
        except Exception as e:
            logger.error(f"Ошибка обработки: {e}")


async def start_incomming_task_consumer():
    connection = await connect_robust(settings.rabbit.rabbit_url)
    channel = await connection.channel()
    queue = await channel.declare_queue(
        settings.rabbit.router_queue_title, durable=True
    )
    await queue.consume(handle_message)
    logger.info("⏳ Консьюмер запущен и слушает очередь")
    return connection
