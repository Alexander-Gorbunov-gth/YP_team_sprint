import json
from logging import getLogger

from aio_pika import DeliveryMode, IncomingMessage, Message, connect_robust
from src.core.config import settings
from src.domain.status import MessageStatus
from src.domain.tasks import MessageToSend
from src.infrastructure.repositories.messages_status import get_short_url_repository
from src.services.email import get_email_sender

logger = getLogger(__name__)


async def email_handle_message(message: IncomingMessage):
    try:
        data = json.loads(message.body.decode())
        headers = message.headers or {}
        x_death_count = 0
        if headers.get("x-death"):
            x_death_count = headers["x-death"][0].get("count", 0)
            logger.info(f"Сообщение Email с адресом {data.get('address')} было отложено {x_death_count} раз")

        logger.info(f"Получено сообщение Email: {data}")
        message_model = MessageToSend(**data)
        sender = get_email_sender(message_model)
        result = await sender.send()

        if result:
            status = MessageStatus.sent

        if not result and x_death_count <= settings.rabbit.max_retry_count:
            logger.error(f"Не удалось отправить Email на адрес {message_model.address}")
            await message.nack(requeue=False)
            return

        if not result:
            status = MessageStatus.error
            logger.error(
                f"Сообщение Email с адресом {message_model.address} не удалось отправить после {x_death_count} попыток"
            )

        repository = await get_short_url_repository()
        await repository.create(
            body=message_model.body,
            sent_to=message_model.user_uuid,
            sent_address=message_model.address,
            subject=message_model.subject,
            status=status,
        )

        await message.ack()

    except Exception as e:
        logger.error(f"Ошибка обработки отправки Email: {e}")
