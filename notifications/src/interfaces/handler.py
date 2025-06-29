from abc import ABC, abstractmethod

from aio_pika import Message
from pydantic import BaseModel


class ConsumeMessage(BaseModel):
    event_name: str


class AbstractHandler(ABC):
    @abstractmethod
    async def handle(self, message: Message) -> None: ...
