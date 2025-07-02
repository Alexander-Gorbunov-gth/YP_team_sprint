import logging
import uuid
from datetime import datetime, timezone

import pytz
from src.domain.clients import Client
from src.domain.tasks import IncomingTaskMessage
from src.domain.templates import Template
from src.infrastructure.container import AppContainer
from src.infrastructure.messages import AbstractMessageMaker

logger = logging.getLogger(__name__)


class MessageMaker(AbstractMessageMaker):

    def __init__(self, task_message: IncomingTaskMessage):
        super().__init__(task_message)

    async def compile(self) -> None:
        """Компилирует класс"""
        self._templates = await self._get_task_templates()
        self._publisher = await AppContainer.get_producer()

    async def _get_task_templates(self) -> dict:
        templates = {}
        for channel in self.task_message.channels:
            template = await self.get_message_template(self.task_message.event_type, channel.value)
            templates[channel.value] = template
        return templates

    async def send_task(self, channel: str, data: Client, body: str, subject: str | None, delay: int) -> None:
        message = {
            "body": body,
            "subject": subject,
            "address": data.get_address(channel),
            "user_uuid": str(data.id),
        }
        queue_name = f"{channel}_message_queue"
        logger.info(f"Send {message} to queue {queue_name} with delay {delay} ms")
        await self._publisher.send(message=message, routing_key=queue_name, delay_ms=delay)

    async def get_message_body(self, template: Template, client_data: dict, params: dict) -> str:
        return template.body.format(**params, **client_data)

    async def get_delay(self, client_timezone: str) -> int:
        send_at: datetime | None = self.task_message.send_at
        if not self.task_message.send_in_local_time and not send_at:
            return 0
        now_utc = datetime.now(timezone.utc)
        # logger.info(f"Текущее время UTC: {now_utc}")
        if self.task_message.send_in_local_time:
            try:
                client_tz = pytz.timezone(client_timezone)
            except pytz.UnknownTimeZoneError:
                logger.warning(f"Неизвестный часовой пояс: {client_timezone}, используется UTC.")
                client_tz = pytz.utc
        else:
            client_tz = pytz.utc
        # logger.info(f"Часовой пояс клиента: {client_timezone}")

        send_at_utc = send_at.astimezone(client_tz)
        logger.info(f"Время отправки в UTC: {send_at_utc}")
        delay_seconds = (send_at_utc - now_utc).total_seconds()
        delay_ms = max(int(delay_seconds * 1000), 0)
        logger.info(f"Задержка отправки сообщения для часового пояса {client_timezone}: {delay_ms} мс")
        return delay_ms

    async def get_message_subject(self, template: Template, client_data: dict, params: dict) -> str:
        if not template.subject:
            return None
        return template.subject.format(**params, **client_data)

    async def get_message_template(self, event_type: str, channel: str) -> Template:
        # Здесь должна быть логика получения шаблона
        return Template(
            id=uuid.uuid4(),
            channel=channel,
            subject="Subject",
            body="Some text",
            event_type=event_type,
        )

    async def run(self, clients_data: list[Client]) -> bool:
        logger.info(f"Запуск формирования сообщений для {len(clients_data)} клиентов")
        for channel, template in self._templates.items():
            for data in clients_data:
                client_uuid = data.id
                params = self.task_message.user_params.get(client_uuid, {})
                # logger.info(f"Получены параметры для клиента {client_uuid}: {params}")
                body: str = await self.get_message_body(template, data.model_dump(), params)
                # logger.info(f"Сформировано тело сообщения: {body}")
                subject: str = await self.get_message_subject(template, data.model_dump(), params)
                delay = await self.get_delay(data.timezone)
                await self.send_task(channel, data, body, subject, delay)


def get_message_maker(task_message: IncomingTaskMessage) -> AbstractMessageMaker:
    return MessageMaker(task_message)
