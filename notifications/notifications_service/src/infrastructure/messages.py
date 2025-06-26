from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.clients import Client
from src.domain.tasks import IncomingTaskMessage
from src.domain.templates import Template


class AbstractMessageMaker(ABC):

    def __init__(self, task_message: IncomingTaskMessage):
        self.task_message = task_message

    @abstractmethod
    async def compile(self) -> None:
        """Компилирует класс"""

    @abstractmethod
    async def send_task(self, message: str, send_to: str, delay: int) -> None:
        """Создает задачу на отправку сообщения."""

    @abstractmethod
    async def get_message_template(self, event_type: str, channel: str) -> Template:
        """Получает шаблон сообщения на основе типа события и канала."""

    @abstractmethod
    async def get_message_body(
        self, template: Template, client_data: dict, params: dict
    ) -> str:
        """Получает тело сообщения на основе типа события и параметров.

        Returns:
            str: Тело сообщения.
        """
        pass

    @abstractmethod
    async def get_message_subject(
        self, template: Template, client_data: dict, params: dict
    ) -> str:
        """Получает тему сообщения на основе типа события и параметров.

        Returns:
            str: Тема сообщения.
        """

    @abstractmethod
    async def get_delay(self, client_timezone: str) -> int:
        """Получает задержку отправки сообщения на основе часового пояса клиента и времени отправки.

        Args:
            client_timezone (str): Часовой пояс клиента.
            send_at (datetime): Время отправки сообщения.

        Returns:
            int: Задержка в милисекундах.
        """

    @abstractmethod
    async def run(self, clients_data: list[Client]) -> bool:
        """Запускает процесс создания и отправки сообщений для списка клиентов."""


class AbstractSender(ABC):

    @abstractmethod
    async def send(
        self, message: str, send_to: str, subject: str | None = None
    ) -> bool:
        """Отправляет сообщение."""
        pass
