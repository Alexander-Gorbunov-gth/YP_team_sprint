import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query

from src.api.v1.depends import CurrentUserDep
from src.api.v1.schemas.subscription import (
    SubscriptionCreateSchema,
    SubscriptionDeleteSchema,
    SubscriptionResponseSchema,
)
from src.services.apps import IAppsService
from src.api.v1.schemas.utils import Author
from src.domain.dtos.subscription import SubscriptionCreateDTO, SubscriptionDeleteDTO
from src.services.subscription import ISubscriptionService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subscribe", tags=["Subscribe"], route_class=DishkaRoute)


@router.get(
    "/my/",
    summary="Получить мои подписки",
    response_model=list[SubscriptionResponseSchema],
)
async def get_user_subscriptions(
    subscription_service: FromDishka[ISubscriptionService],
    user: CurrentUserDep,
    app_service: FromDishka[IAppsService],
    limit: int = Query(default=10, description="Количество подписок"),
    offset: int = Query(default=0, description="Сдвиг"),
):
    """Получить список подписок текущего пользователя"""

    subscriptions = await subscription_service.get_subscriptions_by_user_id(
        user.id, limit, offset
    )
    user_subscriptions = []
    for subscription in subscriptions:
        author_data = await app_service.get_author(subscription.host_id)
        author = (
            Author(**author_data.model_dump())
            if author_data
            else Author(id=subscription.host_id)
        )
        user_subscriptions.append(
            SubscriptionResponseSchema(**subscription.model_dump(), author=author)
        )
    return user_subscriptions


@router.post(
    "/", summary="Подписаться на автора", response_model=SubscriptionResponseSchema
)
async def subscribe(
    subscription_service: FromDishka[ISubscriptionService],
    user: CurrentUserDep,
    subscription_data: SubscriptionCreateSchema,
) -> SubscriptionResponseSchema:
    """Подписаться на автора"""

    subscription_dto = SubscriptionCreateDTO(
        user_id=user.id, host_id=subscription_data.host_id
    )
    subscription = await subscription_service.create_subscription(subscription_dto)
    author = Author(id=subscription_data.host_id)
    return SubscriptionResponseSchema(**subscription.model_dump(), author=author)


@router.delete("/", summary="Отписаться от автора")
async def unsubscribe(
    subscription_service: FromDishka[ISubscriptionService],
    user: CurrentUserDep,
    subscription_data: SubscriptionDeleteSchema,
) -> bool:
    """Отписаться от автора"""

    subscription_dto = SubscriptionDeleteDTO(
        user_id=user.id, host_id=subscription_data.host_id
    )
    await subscription_service.delete_subscription(subscription_dto)
    return True
