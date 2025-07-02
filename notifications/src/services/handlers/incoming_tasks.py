import asyncio
import json
from logging import getLogger

from aio_pika import IncomingMessage, connect_robust
from httpx import AsyncClient
from src.core.config import settings
from src.domain.channels import ChannelTypes
from src.domain.tasks import (  # Импортируем модель IncomingTaskMessage
    IncomingTaskMessage,
)
from src.infrastructure.messages import AbstractMessageMaker
from src.services.clients_data import get_clients_data_service

logger = getLogger(__name__)


async def incoming_handle_message(message: IncomingMessage):
    from src.services.message_maker import get_message_maker

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
                    logger.warning(f"Не переданы данные о пользователе в сообщении {data}")
                    return
                async for clients_data in clients_data_generator:
                    await message_maker.run(clients_data)
        except Exception as e:
            logger.error(f"Ошибка обработки: {e}")
