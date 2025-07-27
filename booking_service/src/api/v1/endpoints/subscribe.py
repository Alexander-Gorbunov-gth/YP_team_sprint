import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query

from src.api.v1.depends import CurrentUserDep
from src.api.v1.schemas.subscription import (
    SubscriptionCreateSchema,
    SubscriptionDeleteSchema,
    SubscriptionResponseSchema,
)
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
    limit: int = Query(default=10, description="Количество подписок"),
    offset: int = Query(default=0, description="Сдвиг"),
):
    """Получить список подписок текущего пользователя"""

    subscriptions = await subscription_service.get_subscriptions_by_user_id(
        user.id, limit, offset
    )
    return [SubscriptionResponseSchema.model_validate(sub) for sub in subscriptions]


@router.post(
    "/", summary="Подписаться на автора", response_model=SubscriptionResponseSchema
)
async def subscribe(
    subscription_service: FromDishka[ISubscriptionService],
    user: CurrentUserDep,
    subscription_data: SubscriptionCreateSchema,
) -> SubscriptionResponseSchema:
    """Подписаться на автора"""

    subscription = await subscription_service.create_subscription(
        SubscriptionCreateDTO(user_id=user.id, host_id=subscription_data.host_id)
    )
    return SubscriptionResponseSchema.model_validate(subscription)


@router.delete("/", summary="Отписаться от автора")
async def unsubscribe(
    subscription_service: FromDishka[ISubscriptionService],
    user: CurrentUserDep,
    subscription_data: SubscriptionDeleteSchema,
) -> bool:
    """Отписаться от автора"""
    await subscription_service.delete_subscription(
        SubscriptionDeleteDTO(user_id=user.id, host_id=subscription_data.host_id)
    )
    return True
