import logging
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query

from src.domain.schemas.subscription import (
    SubscriptionCreateSchema,
    SubscriptionDeleteSchema,
    SubscriptionRepresentSchema,
)
from src.services.subscription import ISubscriptionService
from src.domain.schemas import subscription as schema
from tests.unit.routers_fixture import sub_data1, sub_data2

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subscribe", tags=["Subscribe"], route_class=DishkaRoute)



@router.get("/my/", summary="Получить мои подписки", response_model=list[SubscriptionRepresentSchema])
async def get_user_subscriptions(
    subscription_service: FromDishka[ISubscriptionService],
    user_id: UUID | str,
    limit: int = Query(default=10, description="Количество подписок"),
    offset: int = Query(default=0, description="Сдвиг"),
):
    subscriptions = await subscription_service.get_subscriptions_by_user_id(user_id, limit, offset)
    return [SubscriptionRepresentSchema.model_validate(sub) for sub in subscriptions]


@router.post("/", summary="Подписаться на автора", response_model=SubscriptionRepresentSchema)
async def subscribe(
    subscription_service: FromDishka[ISubscriptionService], user_id: UUID | str, host_id: UUID | str
) -> SubscriptionRepresentSchema:
    subscription = await subscription_service.create_subscription(
        SubscriptionCreateSchema(user_id=user_id, host_id=host_id)
    )

@router.get(
    "/my/",
    summary="Получить мои подписки",
    response_model=list[schema.SubscriptionRepresentSchema],
)
async def get_events():
    return [sub_data1, sub_data2]


@router.post(
    "/",
    summary="Подписаться на автора",
    response_model=schema.SubscriptionRepresentSchema,
)
async def subscribe(data: schema.SubscriptionCreateSchema):
    return sub_data1



@router.delete("/", summary="Отписаться от автора")
async def unsubscribe(
    subscription_service: FromDishka[ISubscriptionService], user_id: UUID | str, host_id: UUID | str
) -> bool:
    await subscription_service.delete_subscription(SubscriptionDeleteSchema(user_id=user_id, host_id=host_id))
    return True
