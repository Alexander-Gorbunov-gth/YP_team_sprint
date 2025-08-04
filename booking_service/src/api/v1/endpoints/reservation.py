import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path

from src.api.v1.depends import CurrentUserDep
from src.api.v1.schemas.reservation import ReservationCreateSchema, ReservationResponseSchema, ReservationUpdateSchema
from src.services.reservation import IReservationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reservation", tags=["Booking"], route_class=DishkaRoute)


@router.post("/", summary="Забронировать место", response_model=ReservationResponseSchema)
async def booking(data: ReservationCreateSchema, reservation_service: FromDishka[IReservationService]):
    return await reservation_service.create(data)


@router.get("/{id}", summary="Получить данные о бронировании", response_model=ReservationResponseSchema)
async def get_booking(
    reservation_service: FromDishka[IReservationService],
    id: str = Path(..., description="ID бронирования"),
):
    return await reservation_service.get_by_id(id)


@router.get("/my/", summary="Получить список моих бронирований", response_model=list[ReservationResponseSchema])
async def get_bookings(
    user: CurrentUserDep,
    reservation_service: FromDishka[IReservationService],
):
    return await reservation_service.get_by_user_id(user.id)


@router.delete("/{id}", summary="Отменить бронирование")
async def delete_booking(
    reservation_service: FromDishka[IReservationService],
    id: str = Path(..., description="ID бронирования"),
) -> bool:
    return await reservation_service.delete(id)


@router.patch("/{id}", summary="Изменить бронирование", response_model=ReservationResponseSchema)
async def update_booking(
    data: ReservationUpdateSchema,
    reservation_service: FromDishka[IReservationService],
    id: str = Path(..., description="ID бронирования"),
):
    return await reservation_service.update(id, data)
