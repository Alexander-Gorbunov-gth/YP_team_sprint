from collections.abc import Iterable
from uuid import UUID

from src.domain.dtos.subscription import SubscriptionCreateDTO, SubscriptionDeleteDTO
from src.domain.entities.subscription import Subscription
from src.services.interfaces.repositories.subscription import ISubscriptionRepository


class FakeSubscriptionRepository(ISubscriptionRepository):
    def __init__(self):
        self.subscriptions = []

    async def get_subscriptions_by_user_id(
        self, user_id: UUID | str, limit: int, offset: int
    ) -> Iterable[Subscription]:
        result = []
        for sub in self.subscriptions:
            if sub.user_id == user_id:
                result.append(sub)

        return result[offset : offset + limit]

    async def create(self, subscription: SubscriptionCreateDTO) -> Subscription:
        created_subscription = Subscription.create(subscription.host_id, subscription.user_id)
        self.subscriptions.append(created_subscription)
        return created_subscription

    async def delete(self, subscription: SubscriptionDeleteDTO) -> None:
        for sub in self.subscriptions:
            if sub.user_id == subscription.user_id and sub.host_id == subscription.host_id:
                self.subscriptions.remove(sub)
                break
