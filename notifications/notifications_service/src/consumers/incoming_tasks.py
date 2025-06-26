import asyncio
import json
from aio_pika import connect_robust, IncomingMessage
from logging import getLogger
from httpx import AsyncClient

from src.infrastructure.messages import AbstractMessageMaker
from src.core.config import settings
from src.domain.tasks import (
    IncomingTaskMessage,
)  # Импортируем модель IncomingTaskMessage
from src.domain.channels import ChannelTypes
from src.services.message_maker import get_message_maker
from src.services.clients_data import get_clients_data_service

logger = getLogger(__name__)


async def handle_message(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            logger.info(f"Получено сообщение: {data}")
            task_message = IncomingTaskMessage(**data)

            message_maker: AbstractMessageMaker = get_message_maker(task_message)
            await message_maker.compile()

            async with AsyncClient() as httpx_client:
                data_service = get_clients_data_service(httpx_client)
                clients_data_generator = data_service.get_clients_data(
                    list(task_message.user_params.keys()), task_message.for_all_users
                )
                if not clients_data_generator:
                    logger.warning(
                        f"Не переданы данные о пользователе в сообщении {data}"
                    )
                    return
                async for clients_data in clients_data_generator:
                    await message_maker.run(clients_data)
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
