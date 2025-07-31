import pytest

from src.services.exceptions import SubscriptionAlreadyExistsError, SubscriptionNotFoundError
from src.services.subscription import SubscriptionService
from tests.fakes.uow import FakeUnitOfWork
from tests.unit.factories import SubscriptionCreateDTOFactory, SubscriptionDeleteDTOFactory


@pytest.fixture
def subscription_create_dto():
    return SubscriptionCreateDTOFactory.build()


@pytest.fixture
def subscription_delete_dto():
    return SubscriptionDeleteDTOFactory.build()


@pytest.fixture
def subscription_service():
    uow = FakeUnitOfWork()
    service = SubscriptionService(uow)
    return service


@pytest.mark.asyncio
async def test_subsbtion_already_exists(subscription_service, subscription_create_dto):
    await subscription_service.create_subscription(subscription_create_dto)
    with pytest.raises(SubscriptionAlreadyExistsError):
        await subscription_service.create_subscription(subscription_create_dto)


@pytest.mark.asyncio
async def test_subsbtion_not_found(subscription_service, subscription_delete_dto):
    with pytest.raises(SubscriptionNotFoundError):
        await subscription_service.delete_subscription(subscription_delete_dto)


@pytest.mark.asyncio
async def test_create_subscription(subscription_service, subscription_create_dto):
    subscription = await subscription_service.create_subscription(subscription_create_dto)
    assert subscription is not None
    assert subscription.id is not None
    assert subscription.host_id is not None
    assert subscription.user_id is not None
    assert subscription.created_at is not None
    assert subscription.updated_at is not None
