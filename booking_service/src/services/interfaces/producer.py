import abc
from uuid import UUID

from pydantic import BaseModel


class PublishMessage(BaseModel):
    user_id: UUID | str


class IProducer(abc.ABC):
    @abc.abstractmethod
    async def publish(self, message: PublishMessage) -> None: ...
