from src.services.interfaces.producer import IProducer
from src.services.interfaces.repositories.address import IAddressRepository
from src.services.interfaces.repositories.event import IEventRepository
from src.services.interfaces.repositories.subscription import ISubscriptionRepository
from src.services.interfaces.uow import IUnitOfWork
from tests.fakes.producer import FakeProducer
from tests.fakes.repositories.address import FakeAddressRepository
from tests.fakes.repositories.event import FakeEventRepository
from tests.fakes.repositories.subscription import FakeSubscriptionRepository


class FakeUnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self._subscription_repository = FakeSubscriptionRepository()
        self._event_repository = FakeEventRepository()
        self._producer = FakeProducer()
        self._address_repository = FakeAddressRepository()

    async def __aenter__(self) -> "FakeUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass

    @property
    def subscription_repository(self) -> ISubscriptionRepository:
        return self._subscription_repository

    @property
    def event_repository(self) -> IEventRepository:
        return self._event_repository

    @property
    def address_repository(self) -> IAddressRepository:
        return self._address_repository

    @property
    def producer(self) -> IProducer:
        return self._producer
