import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from src.domain.schemas import reservation as schema

from tests.unit.routers_fixture import reservation_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reservation", tags=["Booking"])


@router.post("/", summary="Забронировать место", response_model=schema.ReservationRepresentSchema)
async def booking(
    data: schema.ReservationCreateSchema
):
    return reservation_data



@router.get("/{id}", summary="Получить данные о бронировании", response_model=schema.ReservationRepresentSchema)
async def get_booking():
    return reservation_data


@router.get("/my/", summary="Получить список моих бронирований", response_model=list[schema.ReservationRepresentSchema])
async def get_bookings():
    return [reservation_data, reservation_data, reservation_data]

@router.delete("/{id}", summary="Отменить бронирование")
async def delete_booking() -> bool:
    return True


@router.patch("/{id}", summary="Изменить бронирование", response_model=schema.ReservationRepresentSchema)
async def update_booking(
    data: schema.ReservationUpdateSchema
):
    return reservation_data
