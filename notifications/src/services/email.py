from src.domain.tasks import MessageToSend
from src.infrastructure.messages import AbstractSender


class EmailSender(AbstractSender):

    async def send(self) -> bool:
        pass


def get_email_sender(message: MessageToSend) -> AbstractSender:
    return EmailSender(message)
