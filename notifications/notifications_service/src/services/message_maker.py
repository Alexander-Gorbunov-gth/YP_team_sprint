from datetime import datetime
import uuid

from src.infrastructure.messages import AbstractSender, AbstractMessageMaker
from src.domain.tasks import TaskMessage
from src.domain.clients import Client
from src.domain.templates import Template

class MessageMaker(AbstractMessageMaker):

    def __init__(self, task_message: TaskMessage):
        super().__init__(task_message)
        self._templates = await._get_task_templates()

    async def _get_task_templates(self) -> dict:
        templates = {}
        for channel in self.task_message.channels:
            template = await self.get_message_template(self.task_message.event_type, channel)
            templates[channel] = template
        return templates

    async def create_send_task(self, message: str, send_to: str, delay: int) -> bool:
        # Здесь должна быть логика отправки email
        print(f"Sending email to {send_to} with message: {message} after {delay} ms")
        return True

    async def get_message_body(self, template: Template, client_data: dict, params: dict) -> str:
        return f"Email body for event {client_data} with params {params}"

    async def get_delay(self, client_timezone: str) -> int:
        # Здесь должна быть логика вычисления задержки 
        # send_at
        return 1000  # Пример задержки в миллисекундах

    async def get_client_data(self, user_uuid: list[str]) -> list[dict]:
        # Здесь должна быть логика получения данных клиента
        return [{"timezone": "UTC", "email": "test@email.ru"}]

    async def get_message_subject(self, template: Template, client_data: dict, params: dict) -> str:
        return f"Email subject for event {event_type} with params {params}"
    
    async def get_message_template(self, event_type: str, channel: str) -> Template:
        # Здесь должна быть логика получения шаблона
        return Template(id=uuid.uuid4(), channel=channel, subject="Subject", body="Some text")

    async def run(self, clients_data: list[Client]) -> bool:
        for channel, template in self._templates.items():
            for data in clients_data:
                client_uuid = data.get("uuid")
                params = self.task_message.params.get(client_uuid, {})
                body: str = await self.get_message_body(template, data, params)
                subject: str = await self.get_message_subject(template, data, params)
                delay = await self.get_delay(data.get("timezone"))
                if await self.create_send_task(body, data.get("email"), delay):
                    return True




class EmailSender(AbstractSender):

    async def send(self, message: str, send_to: str, subject: str) -> bool:
        pass


def get_message_maker(task_message: TaskMessage) -> AbstractMessageMaker:
    return MessageMaker(task_message)
