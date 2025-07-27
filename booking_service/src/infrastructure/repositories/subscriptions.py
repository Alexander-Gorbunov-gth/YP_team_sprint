import logging
from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import Result, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.subscription import Subscription
from src.api.v1.schemas.subscription import (
    SubscriptionCreateSchema,
    SubscriptionDeleteSchema,
)
from src.infrastructure.repositories.exceptions import (
    SubscriptionAlreadyExistsError,
    SubscriptionNotFoundError,
)
from src.services.interfaces.repositories.subscription import ISubscriptionRepository

logger = logging.getLogger(__name__)


class SQLAlchemySubscriptionRepository(ISubscriptionRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, subscription: SubscriptionCreateSchema) -> Subscription:
        """
        Создает подписку в базе данных.
        :param subscription: Схема подписки для создания.
        :raises SubscriptionAlreadyExistsError: Если подписка уже существует.
        :return: Созданная подписка.
        """

        check_query = select(Subscription).filter_by(
            host_id=subscription.host_id, user_id=subscription.user_id
        )
        result: Result = await self._session.execute(check_query)
        existing = result.scalar_one_or_none()
        if existing:
            raise SubscriptionAlreadyExistsError(
                f"Подписка {subscription.host_id=} {subscription.user_id=} уже существует"
            )

        query = (
            insert(Subscription)
            .values(subscription.model_dump())
            .returning(Subscription)
        )
        created_subscription: Result = await self._session.execute(query)
        return created_subscription.scalar_one()

    async def delete(self, subscription: SubscriptionDeleteSchema) -> None:
        """
        Удаляет подписку из базы данных.
        :param subscription: Схема подписки для удаления.
        :raises SubscriptionNotFoundError: Если подписка не найдена.
        """

        check_query = select(Subscription).filter_by(
            host_id=subscription.host_id, user_id=subscription.user_id
        )
        result: Result = await self._session.execute(check_query)
        existing = result.scalar_one_or_none()
        if existing is None:
            raise SubscriptionNotFoundError(
                f"Подписка с {subscription.host_id=} и {subscription.user_id=} не найдена."
            )
        await self._session.delete(subscription)

    async def get_subscriptions_by_user_id(
        self, user_id: UUID | str, limit: int, offset: int
    ) -> Iterable[Subscription]:
        """
        Получает все подписки для пользователя.
        :param user_id: ID пользователя.
        :return: Список подписок.
        """

        query = (
            select(Subscription)
            .filter_by(user_id=user_id)
            .limit(limit)
            .offset(offset)
            .order_by(Subscription.created_at.desc())  # type: ignore
        )
        result: Result = await self._session.execute(query)
        return result.unique().scalars().all()
