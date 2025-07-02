import logging
from email.message import EmailMessage

import aiosmtplib
import backoff
from src.core.config import settings
from src.domain.tasks import MessageToSend
from src.infrastructure.messages import AbstractSender

logger = logging.getLogger(__name__)


class EmailSender(AbstractSender):

    @backoff.on_exception(
        backoff.expo,
        (aiosmtplib.SMTPException, ConnectionError, TimeoutError),
        max_tries=2,
        jitter=None,
        on_backoff=lambda details: logger.warning(
            f"🔁 Повторная попытка отправки Email ({details['tries']}): " f"{details.get('exception')}"
        ),
    )
    async def send(self) -> bool:
        message = EmailMessage()
        message["Subject"] = self.message.subject
        message["From"] = settings.email.from_address
        message["To"] = self.message.address
        message.set_content(self.message.body)
        logger.info(f"📧 Отправка Email на адрес {self.message.address}")
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
