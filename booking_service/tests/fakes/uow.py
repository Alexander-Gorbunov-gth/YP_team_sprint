from src.services.interfaces.producer import IProducer
from src.services.interfaces.repositories.event import IEventRepository
from src.services.interfaces.uow import IUnitOfWork
from tests.fakes.producer import FakeProducer
from tests.fakes.repositories.event import FakeEventRepository


class FakeUnitOfWork(IUnitOfWork):
    async def __aenter__(self) -> "FakeUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    @property
    def event_repository(self) -> IEventRepository:
        return FakeEventRepository()

    @property
    def producer(self) -> IProducer:
        return FakeProducer()
