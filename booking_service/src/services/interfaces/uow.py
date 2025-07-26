from abc import ABC, abstractmethod

from src.services.interfaces.repositories.subscription import ISubscriptionRepository


class IUnitOfWork(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork": ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> None: ...

    @property
    @abstractmethod
    def subscription_repository(self) -> ISubscriptionRepository: ...
