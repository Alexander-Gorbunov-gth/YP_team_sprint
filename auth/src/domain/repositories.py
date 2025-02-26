from abc import ABC, abstractmethod

from src.domain.entities import User


class AbstractUserRepository(ABC):
    @abstractmethod
    def create(email: str, password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(user_id: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def update(user: User) -> User:
        raise NotImplementedError
