from abc import ABC, abstractmethod
from typing import AsyncGenerator

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.interfaces.messaging.producer import AbstractProducer


class AbstractContainer(ABC):
    @abstractmethod
    async def startup(self) -> None: ...

    @abstractmethod
    async def shutdown(self) -> None: ...

    @abstractmethod
    async def get_producer(self) -> AbstractProducer: ...

    @abstractmethod
    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]: ...

    @abstractmethod
    async def get_http_client(self) -> AsyncGenerator[AsyncClient, None]: ...
