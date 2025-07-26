import logging
from uuid import UUID

from fastapi import Depends
from sqlalchemy import Result, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.domain.entities.subscription import Subscription
from src.services.interfaces.repositories.subscription import ISubscriptionRepository

logger = logging.getLogger(__name__)


class SQLAlchemySubscriptionRepository(ISubscriptionRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(
        self,
        host_id: UUID,
        user_id: UUID,
        # TODO: Применить схему SubscriptionCreateSchema
    ) -> Subscription:
        check_query = select(Subscription).filter_by(host_id=host_id, user_id=user_id)
        existing: Result = await self._session.execute(check_query)
        subscription = existing.scalar_one_or_none()

        if subscription:
            logger.warning(f"Добавляемый Subscription с host_id={host_id}, " + f"user_id={user_id} уже существует.")
            return subscription

        query = insert(Subscription).values({"host_id": host_id, "user_id": user_id}).returning(Subscription)
        result: Result = await self._session.execute(query)
        await self._commit()
        return result.scalar_one()

    async def get_subscriptions_by_user_id(
        self,
        user_id: UUID | str,
    ) -> list[Subscription]:
        query = select(Subscription).filter_by(user_id=user_id)
        result: Result = await self._session.execute(query)
        return result.unique().scalars().all()

    async def delete(
        self,
        host_id: UUID,
        user_id: UUID,
        # TODO: Применить схему SubscriptionDeleteSchema
    ) -> Subscription | None:
        query = select(Subscription).filter_by(user_id=user_id, host_id=host_id)
        result: Result = await self._session.execute(query)
        subscription = result.scalar_one_or_none()

        if subscription is None:
            logger.warning(f"Удаляемый Subscription с user_id={user_id}, " + f"host_id={host_id} не найден.")
            return None

        await self._session.delete(subscription)
        await self._commit()
        return subscription

    async def _commit(self) -> None:
        await self._session.commit()


async def get_subscription_repository(session: AsyncSession = Depends(get_session)) -> SQLAlchemySubscriptionRepository:
    return SQLAlchemySubscriptionRepository(session=session)
