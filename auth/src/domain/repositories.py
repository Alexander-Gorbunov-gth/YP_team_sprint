from abc import ABC, abstractmethod
from datetime import timedelta

from src.domain.entities import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, email: str, password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, user: User) -> User:
        raise NotImplementedError


class BlackListRepository(ABC):
    @abstractmethod
    async def exists(self, token: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def add(self, token: str, expire: timedelta) -> None:
        raise NotImplementedError
