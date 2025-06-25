from datetime import datetime

from src.infrastructure.messages import AbstractSender, AbstractMessageMaker


class EmailMessageMaker(AbstractMessageMaker):
    async def create_send_task(self, message: str, send_to: str, delay: int) -> bool:
        # Здесь должна быть логика отправки email
        print(f"Sending email to {send_to} with message: {message} after {delay} ms")
        return True

    async def get_message_body(self, event_type: str, params: dict) -> str:
        return f"Email body for event {event_type} with params {params}"

    async def get_delay(self, client_timezone: str, send_at: datetime) -> int:
        # Здесь должна быть логика вычисления задержки
        return 1000  # Пример задержки в миллисекундах

    async def get_client_data(self, user_uuid: list[str]) -> list[dict]:
        # Здесь должна быть логика получения данных клиента
        return [{"timezone": "UTC", "email": "test@email.ru"}]

    async def get_message_subject(self, event_type: str, params: dict) -> str:
        return f"Email subject for event {event_type} with params {params}"


class EmailSender(AbstractSender):

    async def send(self, message: str, send_to: str, subject: str) -> bool:
        pass


def get_email_message_maker() -> EmailMessageMaker:
    return EmailMessageMaker()
