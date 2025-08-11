import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path

from src.api.v1.depends import CurrentUserDep
from src.domain.entities.reservation import Reservation
from src.api.v1.schemas.reservation import (
    ReservationCreateSchema,
    ReservationResponseSchema,
    ReservationUpdateSchema,
    ReservationFullResponseSchema,
)
from src.domain.entities.reservation import ReservationStatus
from src.domain.entities.movie import Movie
from src.domain.entities.event import Event
from src.api.v1.schemas.utils import MovieSchema
from src.services.event import IEventService
from src.services.apps import IAppsService
from src.services.reservation import IReservationService
from src.domain.exceptions import NotAvailable

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reservation", tags=["Booking"], route_class=DishkaRoute)


@router.get(
    "/{id}",
    summary="Получить данные о бронировании",
    response_model=ReservationFullResponseSchema,
)
async def get_booking(
    reservation_service: FromDishka[IReservationService],
    event_service: FromDishka[IEventService],
    movie_service: FromDishka[IAppsService],
    current_user: CurrentUserDep,
    id: str = Path(..., description="ID бронирования"),
):
    reservation: Reservation = await reservation_service.get_by_id(id)
    event_id = reservation.event_id
    event = await event_service.get_by_id(event_id)
    movie_data: Movie = await movie_service.get_film(event.movie_id)
    movie = MovieSchema(**movie_data.model_dump())
    return ReservationFullResponseSchema(movie=movie, **reservation.model_dump())


@router.get(
    "/my/",
    summary="Получить список моих бронирований",
    response_model=list[ReservationResponseSchema],
)
async def get_bookings(
    user: CurrentUserDep,
    movie_service: FromDishka[IAppsService],
    event_service: FromDishka[IEventService],
    reservation_service: FromDishka[IReservationService],
):
    reservations = await reservation_service.get_by_user_id(user.id)
    response = []
    for reservation in reservations:
        event_id = reservation.event_id
        event = await event_service.get_by_id(event_id)
        movie_data: Movie = await movie_service.get_film(event.movie_id)
        response.append(
            ReservationResponseSchema(
                **reservation.model_dump(),
                movie_title=movie_data.title,
            )
        )
    return response


@router.delete("/{id}", summary="Отменить бронирование")
async def delete_booking(
    reservation_service: FromDishka[IReservationService],
    current_user: CurrentUserDep,
    id: str = Path(..., description="ID бронирования"),
) -> bool:
    return await reservation_service.delete(id)


@router.patch(
    "/{id}", summary="Изменить бронирование", response_model=ReservationResponseSchema
)
async def update_booking(
    data: ReservationUpdateSchema,
    current_user: CurrentUserDep,
    event_service: FromDishka[IEventService],
    reservation_service: FromDishka[IReservationService],
    id: str = Path(..., description="ID бронирования"),
):
    reservation: Reservation = await reservation_service.get_by_id(id)
    event_id = reservation.event_id
    event: Event = await event_service.get_by_id(event_id)
    user_id = current_user.id
    if data.status == ReservationStatus.SUCCESS and event.owner_id != user_id:
        raise NotAvailable
    return await reservation_service.update(
        reservation_id=id, reservation=data, user_id=reservation.user_id
    )
