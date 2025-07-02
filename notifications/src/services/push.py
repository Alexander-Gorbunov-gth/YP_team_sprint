from src.domain.tasks import MessageToSend
from src.infrastructure.messages import AbstractSender


class PushSender(AbstractSender):

    async def send(self) -> bool:
        pass


def get_push_sender(message: MessageToSend) -> AbstractSender:
    return PushSender(message)
