import logging

from fastapi import APIRouter

from src.domain.schemas import subscription as schema
from tests.unit.routers_fixture import sub_data1, sub_data2

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subscribe", tags=["Subscribe"])


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
async def unsubscribe(data: schema.SubscriptionDeleteSchema) -> bool:
    return True
