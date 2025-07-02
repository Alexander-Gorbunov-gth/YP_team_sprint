import logging

from pydantic import ValidationError
from src.interfaces.handler import AbstractHandler, ConsumeMessage
from aio_pika import IncomingMessage, connect_robust, Message, DeliveryMode

logger = logging.getLogger(__name__)


class PushHandler(AbstractHandler):
    async def handle(self, message: Message) -> None:
        try:
            consume_message = ConsumeMessage.model_validate_json(message.body)
            logger.info(f"✅ Сообщение успешно провалидировано: {consume_message}")
        except ValidationError as e:
            logger.error(f"❌ Ошибка при валидации сообщения: {e}")


async def push_handle_message(message: IncomingMessage) -> None:
    pass
