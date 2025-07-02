import json
import logging
from uuid import UUID

from aio_pika import IncomingMessage
from fastapi import WebSocket
from src.core.config import settings
from src.domain.status import MessageStatus
from src.domain.tasks import MessageToSend
from src.infrastructure.repositories.messages_status import get_short_url_repository
from src.services.push import get_push_sender

logger = logging.getLogger(__name__)


active_connections: dict[UUID, WebSocket] = {}


async def push_handle_message(message: IncomingMessage) -> None:
    data = json.loads(message.body.decode())
    message = MessageToSend(**data)
    if active_connections.get(message.user_uuid):
        websocket = active_connections.get(message.user_uuid)
        sender = get_push_sender(message, websocket)
        result = await sender.send()
        if result:
            status = MessageStatus.sent
        else:
            status = MessageStatus.error
    else:
        status = MessageStatus.error
        logger.error(f"Не удалось отправить push на адрес {message.address}. Пользователь не активен.")
        return

    repository = await get_short_url_repository()
    await repository.create(
        body=message.body,
        sent_to=message.user_uuid,
        sent_address=message.address,
        subject=message.subject,
        status=status,
    )
