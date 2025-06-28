from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime

from src.domain.status import MessageStatus, MessageModel


class AbstractMessagesStatusRepository(ABC):

    @abstractmethod
    async def create(
        self,
        body: str,
        sent_to: UUID,
        sent_address: str,
        status: MessageStatus,
        subject: str
    ) -> MessageModel:
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, id: UUID, status: MessageStatus) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_send_at(self, id: UUID, send_at: datetime) -> None:
        raise NotImplementedError
