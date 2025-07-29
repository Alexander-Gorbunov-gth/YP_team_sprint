import abc
from collections.abc import Iterable
from uuid import UUID

from src.domain.dtos.subscription import SubscriptionCreateDTO, SubscriptionDeleteDTO
from src.domain.entities.subscription import Subscription


class ISubscriptionRepository(abc.ABC):
    @abc.abstractmethod
    async def get_subscriptions_by_user_id(
        self, user_id: UUID | str, limit: int, offset: int
    ) -> Iterable[Subscription]: ...

    @abc.abstractmethod
    async def create(self, subscription: SubscriptionCreateDTO) -> Subscription | None: ...

    @abc.abstractmethod
    async def delete(self, subscription: SubscriptionDeleteDTO) -> Subscription | None: ...
