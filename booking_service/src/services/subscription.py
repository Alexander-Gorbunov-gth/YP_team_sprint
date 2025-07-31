import abc
from collections.abc import Iterable
from uuid import UUID

from src.domain.entities.subscription import Subscription
from src.domain.dtos.subscription import SubscriptionCreateDTO, SubscriptionDeleteDTO
from src.services.interfaces.uow import IUnitOfWork


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
            return Subscription.model_validate(
                await uow.subscription_repository.create(subscription))

    async def delete_subscription(self, subscription: SubscriptionDeleteDTOw) -> None:
        async with self._uow as uow:
            await uow.subscription_repository.delete(subscription)

    async def get_subscriptions_by_user_id(
        self, user_id: UUID | str, limit: int, offset: int
    ) -> Iterable[Subscription]:
        async with self._uow as uow:
            return await uow.subscription_repository.get_subscriptions_by_user_id(
                user_id=user_id, limit=limit, offset=offset
            )
