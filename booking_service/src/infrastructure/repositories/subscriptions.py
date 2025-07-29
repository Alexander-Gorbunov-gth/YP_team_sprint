import logging
from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import Result, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.dtos.subscription import SubscriptionCreateDTO, SubscriptionDeleteDTO
from src.domain.entities.subscription import Subscription
from src.services.interfaces.repositories.subscription import ISubscriptionRepository

logger = logging.getLogger(__name__)


class SQLAlchemySubscriptionRepository(ISubscriptionRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def _check_subscription(self, host_id: UUID, user_id: UUID) -> Subscription | None:
        check_query = select(Subscription).filter_by(host_id=host_id, user_id=user_id)
        result: Result = await self._session.execute(check_query)
        return result.scalar_one_or_none()

    async def create(self, subscription: SubscriptionCreateDTO) -> Subscription | None:
        """
        Создает подписку в базе данных.
        :param subscription: Схема подписки для создания.
        :raises SubscriptionAlreadyExistsError: Если подписка уже существует.
        :return: Созданная подписка.
        """

        existing = await self._check_subscription(subscription.host_id, subscription.user_id)
        if existing is not None:
            return None
        query = insert(Subscription).values(subscription.model_dump()).returning(Subscription)
        created_subscription: Result = await self._session.execute(query)
        return created_subscription.scalar_one()

    async def delete(self, subscription: SubscriptionDeleteDTO) -> Subscription | None:
        """
        Удаляет подписку из базы данных.
        :param subscription: Схема подписки для удаления.
        :raises SubscriptionNotFoundError: Если подписка не найдена.
        """

        existing = await self._check_subscription(subscription.host_id, subscription.user_id)
        if existing is None:
            return None
        delete_query = (
            delete(Subscription)
            .filter_by(host_id=subscription.host_id, user_id=subscription.user_id)
            .returning(Subscription)
        )
        deleted_subscription: Result = await self._session.execute(delete_query)
        return deleted_subscription.scalar_one_or_none()

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
