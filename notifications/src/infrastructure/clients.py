from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.clients import Client
from src.domain.tasks import IncomingTaskMessage


class AbstractDataClientsService(ABC):
    @abstractmethod
    async def get_clients_data(self, message: IncomingTaskMessage) -> list[Client]: ...
