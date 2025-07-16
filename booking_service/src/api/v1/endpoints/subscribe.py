import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
# from src.api.v1.schemas.events import

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subscribe", tags=["Subscribe"])


@router.get("/my/{uuid}", summary="Получить мои подписки")
async def get_events():
    return


@router.get("/{uuid}", summary="Получить данные о подписке на автора")
async def get_subscribe():
    return

@router.post("/{uuid}", summary="Подписаться на автора")
async def subscribe():
    return

@router.delete("/{uuid}", summary="Отписаться от автора")
async def unsubscribe():
    return


