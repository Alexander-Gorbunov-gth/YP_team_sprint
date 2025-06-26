from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.tasks import TaskMessage
from src.domain.clients import ClientsData


class AbstractDataClientsService(ABC):
    @abstractmethod
    async def get_clients_data(self, message: TaskMessage) -> list[ClientsData]: ...