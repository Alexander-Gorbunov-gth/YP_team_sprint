import abc
from uuid import UUID

from src.domain.entities.subscription import Subscription
from src.domain.schemas.subscription import SubscriptionCreateSchema, SubscriptionDeleteSchema


class ISubscriptionRepository(abc.ABC):
    @abc.abstractmethod
    async def get_subscriptions_by_user_id(self, user_id: UUID | str) -> list[Subscription]: ...

    @abc.abstractmethod
    async def create(self, subscription: SubscriptionCreateSchema) -> Subscription: ...

    @abc.abstractmethod
    async def delete(self, subscription: SubscriptionDeleteSchema) -> Subscription: ...
