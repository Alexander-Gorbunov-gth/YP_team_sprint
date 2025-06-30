import logging
import aiosmtplib
from email.message import EmailMessage

from src.core import logger
from src.domain.tasks import MessageToSend
from src.infrastructure.messages import AbstractSender

from src.core.config import settings

logger = logging.getLogger(__name__)


class EmailSender(AbstractSender):

    async def send(self) -> bool:
        message = EmailMessage()
        message["Subject"] = self.message.subject
        message["From"] = settings.email.from_address
        message["To"] = self.message.address
        message.set_content(self.message.body)
        try:
            await aiosmtplib.send(
                message,
                hostname=settings.email.smtp_host,
                port=settings.email.smtp_port,
                username=settings.email.smtp_user,
                password=settings.email.smtp_password,
            )
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке Email: {e}")
            return False


def get_email_sender(message: MessageToSend) -> AbstractSender:
    return EmailSender(message)
