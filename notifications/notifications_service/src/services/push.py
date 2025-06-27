from src.infrastructure.messages import AbstractSender
from src.domain.tasks import MessageToSend



class PushSender(AbstractSender):

    async def send(self) -> bool:
        pass



def get_email_sender(message: MessageToSend) -> AbstractSender:
    return PushSender(message)