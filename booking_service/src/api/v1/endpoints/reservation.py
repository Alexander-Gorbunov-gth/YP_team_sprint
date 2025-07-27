import logging

from fastapi import APIRouter

from src.api.v1.schemas.reservation import ReservationCreateSchema, ReservationResponseSchema, ReservationUpdateSchema
from tests.unit.routers_fixture import reservation_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reservation", tags=["Booking"])


@router.post("/", summary="Забронировать место", response_model=ReservationResponseSchema)
async def booking(data: ReservationCreateSchema):
    return reservation_data


@router.get("/{id}", summary="Получить данные о бронировании", response_model=ReservationResponseSchema)
async def get_booking():
    return reservation_data


@router.get("/my/", summary="Получить список моих бронирований", response_model=list[ReservationResponseSchema])
async def get_bookings():
    return [reservation_data, reservation_data, reservation_data]


@router.delete("/{id}", summary="Отменить бронирование")
async def delete_booking() -> bool:
    return True


@router.patch("/{id}", summary="Изменить бронирование", response_model=ReservationResponseSchema)
async def update_booking(data: ReservationUpdateSchema):
    return reservation_data
