from abc import ABC, abstractmethod
from datetime import datetime


class AbstractMessageMaker(ABC):

    @abstractmethod
    async def create_send_task(self, message: str, send_to: str, delay: int) -> bool:
        """Создает задачу на отправку сообщения.

        Args:
            message (str): Сообщение, которое нужно отправить.
            send_to (str): Адрес получателя, например email или номер телефона.
            delay (int): Задержка отправки в миллисекундах.

        Returns:
            bool: True, если сообщение успешно отправлено, иначе False.
        """
        pass

    @abstractmethod
    async def get_message_body(self, event_type: str, params: dict) -> str:
        """Получает тело сообщения на основе типа события и параметров.

        Args:
            event_type (str): Тип события, например 'send_notification'.
            params (dict): Параметры события, которые могут быть использованы в обработчике.

        Returns:
            str: Тело сообщения.
        """
        pass

    async def get_message_subject(self, event_type: str, params: dict) -> str:
        """Получает тему сообщения на основе типа события и параметров.

        Args:
            event_type (str): Тип события, например 'send_notification'.
            params (dict): Параметры события, которые могут быть использованы в обработчике.

        Returns:
            str: Тема сообщения.
        """
        return f"Notification for {event_type}"

    @abstractmethod
    async def get_delay(self, client_timezone: str, send_at: datetime) -> int:
        """Получает задержку отправки сообщения на основе часового пояса клиента и времени отправки.

        Args:
            client_timezone (str): Часовой пояс клиента.
            send_at (datetime): Время отправки сообщения.

        Returns:
            int: Задержка в милисекундах.
        """
        pass

    @abstractmethod
    async def get_client_data(self, user_uuid: list[str]) -> list[dict]:
        """Получает данные клиентов на основе их уникальных идентификаторов.

        Args:
            user_uuid (list[str]): Список уникальных идентификаторов клиентов.

        Returns:
            dict: Данные клиентов, например email и часовой пояс.
        """
        pass


class AbstractSender(ABC):

    @abstractmethod
    async def send(
        self, message: str, send_to: str, subject: str | None = None
    ) -> bool:
        """Отправляет сообщение."""
        pass
