from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from src.domain.status import MessageModel, MessageStatus


class AbstractMessagesStatusRepository(ABC):

    @abstractmethod
    async def create(
        self, body: str, sent_to: UUID, sent_address: str, status: MessageStatus, subject: str
    ) -> MessageModel:
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, id: UUID, status: MessageStatus) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_send_at(self, id: UUID, send_at: datetime) -> None:
        raise NotImplementedError
