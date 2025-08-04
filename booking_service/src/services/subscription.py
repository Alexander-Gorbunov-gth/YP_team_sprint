import abc
import logging
from collections.abc import Iterable
from uuid import UUID

from src.domain.dtos.subscription import SubscriptionCreateDTO, SubscriptionDeleteDTO
from src.domain.entities.subscription import Subscription
from src.services.exceptions import SubscriptionNotFoundError, SubscriptionAlreadyExistsError
from src.services.interfaces.uow import IUnitOfWork

logger = logging.getLogger(__name__)


class ISubscriptionService(abc.ABC):
    @abc.abstractmethod
    async def create_subscription(self, subscription: SubscriptionCreateDTO) -> Subscription: ...

    @abc.abstractmethod
    async def delete_subscription(self, subscription: SubscriptionDeleteDTO) -> None: ...

    @abc.abstractmethod
    async def get_subscriptions_by_user_id(
        self, user_id: UUID | str, limit: int, offset: int
    ) -> Iterable[Subscription]: ...


class SubscriptionService(ISubscriptionService):
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def create_subscription(self, subscription: SubscriptionCreateDTO) -> Subscription:
        async with self._uow as uow:
            created_subscription = await uow.subscription_repository.create(subscription)
            if created_subscription is None:
                logger.warning(
                    "Подписка с host_id=%s и user_id=%s уже существует", subscription.host_id, subscription.user_id
                )
                raise SubscriptionAlreadyExistsError("Подписка уже существует")
            return created_subscription

    async def delete_subscription(self, subscription: SubscriptionDeleteDTO) -> None:
        async with self._uow as uow:
            deleted_subscription = await uow.subscription_repository.delete(subscription)
            if deleted_subscription is None:
                logger.warning(
                    "Подписка с host_id=%s и user_id=%s не найдена", subscription.host_id, subscription.user_id
                )
                raise SubscriptionNotFoundError("Подписка не найдена")

    async def get_subscriptions_by_user_id(
        self, user_id: UUID | str, limit: int, offset: int
    ) -> Iterable[Subscription]:
        async with self._uow as uow:
            return await uow.subscription_repository.get_subscriptions_by_user_id(
                user_id=user_id, limit=limit, offset=offset
            )
