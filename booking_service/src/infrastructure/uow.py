from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.infrastructure.messaging.producer import RabbitMQProducer
from src.infrastructure.repositories.events import SQLAlchemyEventRepository
from src.infrastructure.repositories.reservations import SQLAlchemyReservationRepository
from src.infrastructure.repositories.subscriptions import SQLAlchemySubscriptionRepository
from src.services.interfaces.producer import IProducer
from src.services.interfaces.repositories.event import IEventRepository
from src.services.interfaces.repositories.reservation import IReservationRepository
from src.services.interfaces.repositories.subscription import ISubscriptionRepository
from src.services.interfaces.uow import IUnitOfWork


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        if self.session.is_active:
            await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @property
    def producer(self) -> IProducer:
        return RabbitMQProducer(settings.rabbit.connection_url, settings.rabbit.exchange_name)

    @property
    def subscription_repository(self) -> ISubscriptionRepository:
        return SQLAlchemySubscriptionRepository(self.session)

    @property
    def event_repository(self) -> IEventRepository:
        return SQLAlchemyEventRepository(self.session)

    @property
    def reservation_repository(self) -> IReservationRepository:
        return SQLAlchemyReservationRepository(self.session)
