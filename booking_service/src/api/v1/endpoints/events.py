import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
# from src.api.v1.schemas.events import

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", summary="Создать мероприятие")
async def create_event():
    return


@router.get("/", summary="Получить список мероприятий")
async def get_events():
    return


@router.get("/{uuid}", summary="Получить данные о мероприятии")
async def get_event():
    # здесь же будут приходит и данные о бронях и их статусах
    return


@router.delete("/{uuid}", summary="Удалить мероприятие")
async def delete_event():
    return


@router.patch("/{uuid}", summary="Обновить мероприятие")
async def update_event():
    return

