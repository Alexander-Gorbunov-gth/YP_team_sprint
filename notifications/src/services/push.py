import logging

from fastapi import WebSocket
from src.domain.tasks import MessageToSend
from src.infrastructure.messages import AbstractSender

logger = logging.getLogger(__name__)


class PushSender(AbstractSender):
    def __init__(self, message: MessageToSend, websocket: WebSocket):
        self.message = message
        self.websocket = websocket

    async def send(self) -> bool:
        try:
            await self.websocket.send_text(self.message.body)
            return True
        except Exception as e:
            logger.error(f"Ошибка при отправке push: {e}")
            return False


def get_push_sender(message: MessageToSend, websocket: WebSocket) -> AbstractSender:
    return PushSender(message, websocket)
