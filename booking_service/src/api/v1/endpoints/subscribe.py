import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from src.domain.schemas import subscription as schema
from tests.unit.routers_fixture import sub_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subscribe", tags=["Subscribe"])


@router.get("/my/", summary="Получить мои подписки", response_model=list[schema.SubscriptionRepresentSchema])
async def get_events():
    return [sub_data, sub_data, sub_data]


@router.post("/", summary="Подписаться на автора", response_model=schema.SubscriptionRepresentSchema)
async def subscribe(
    data: schema.SubscriptionCreateSchema
):
    return sub_data


@router.delete("/", summary="Отписаться от автора")
async def unsubscribe(
    data: schema.SubscriptionDeleteSchema
) -> bool:
    return True
