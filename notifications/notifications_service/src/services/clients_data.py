from src.infrastructure.clients import AbstractDataClientsService
from src.domain.clients import ClientsData
from src.domain.tasks import TaskMessage

class HttpxClientsDataService(AbstractDataClientsService):
    
    async def get_clients_data(self, message: TaskMessage) -> list[ClientsData]:
        if message.for_all_users:
            return pass
        return []