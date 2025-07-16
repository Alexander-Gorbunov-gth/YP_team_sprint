import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
# from src.api.v1.schemas.events import

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/booking", tags=["Booking"])


@router.post("/", summary="Забронировать место")
async def booking():
    return



@router.get("/{uuid}", summary="Получить данные о бронировании")
async def get_booking():
    return


@router.get("/my/{uuid}", summary="Получить список моих бронирований")
async def get_bookings():
    return

@router.delete("/{uuid}", summary="Отменить бронирование")
async def delete_booking():
    return


@router.patch("/{uuid}", summary="Изменить бронирование")
async def update_booking():
    return