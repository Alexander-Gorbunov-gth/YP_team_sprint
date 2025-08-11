import asyncio
import asyncio
import logging
from uuid import UUID
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Path, Query

from src.api.v1.depends import CurrentUserDep
from src.api.v1.schemas.event import (
    EventCreateSchema,
    EventResponseSchema,
    EventUpdateSchema,
)
from src.api.v1.schemas.reservation import (
    ReservationCreateSchema,
    ReservationResponseSchema,
)
from src.api.v1.schemas.utils import Author, MovieSchema
from src.domain.dtos.event import EventCreateDTO, EventGetAllDTO, EventUpdateDTO
from src.domain.entities.event import Event
from src.domain.entities.movie import Movie
from src.api.v1.schemas.utils import Author, MovieSchema
from src.domain.dtos.event import EventCreateDTO, EventGetAllDTO, EventUpdateDTO
from src.domain.entities.event import Event
from src.domain.entities.movie import Movie
from src.infrastructure.handlers.exceptions import EventNotFoundError
from src.services.apps import IAppsService
from src.services.event import IEventService
from src.services.apps import IAppsService
from src.services.event import IEventService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"], route_class=DishkaRoute)


async def to_schema(event: Event, user_id: UUID, app_service: IAppsService) -> EventResponseSchema:
    # Получаем автора
    author_data = await app_service.get_author(event.owner_id)
    author = Author.model_validate(author_data) if author_data else Author(id=event.owner_id)

    # Получаем фильм
    movie_data: Movie | None = await app_service.get_film(event.movie_id)
    movie = MovieSchema.model_validate(movie_data) if movie_data else MovieSchema(id=event.movie_id)

    # Фильтруем брони
    reservations_filtered = [
        ReservationResponseSchema(**r.model_dump())
        for r in event.reservations
        if r.user_id == user_id or event.owner_id == user_id
    ]

    # Собираем финальный объект
    return EventResponseSchema(
        **event.model_dump(exclude={"address", "reservations"}),
        author=author,
        movie=movie,
        address=event.get_address_for_user(user_id=user_id),
        available_seats=event.available_seats(),
        reservations=reservations_filtered
    )


async def to_schema(event: Event, user_id: UUID, app_service: IAppsService) -> EventResponseSchema:
    # Получаем автора
    author_data = await app_service.get_author(event.owner_id)
    author = Author.model_validate(author_data) if author_data else Author(id=event.owner_id)

    # Получаем фильм
    movie_data: Movie | None = await app_service.get_film(event.movie_id)
    movie = MovieSchema.model_validate(movie_data) if movie_data else MovieSchema(id=event.movie_id)

    # Фильтруем брони
    reservations_filtered = [
        ReservationResponseSchema(**r.model_dump())
        for r in event.reservations
        if r.user_id == user_id or event.owner_id == user_id
    ]

    # Собираем финальный объект
    return EventResponseSchema(
        **event.model_dump(exclude={"address", "reservations"}),
        author=author,
        movie=movie,
        address=event.get_address_for_user(user_id=user_id),
        available_seats=event.available_seats(),
        reservations=reservations_filtered
    )


@router.post("/", summary="Создать мероприятие", response_model=EventResponseSchema)
async def create_event(
    event_service: FromDishka[IEventService],
    app_service: FromDishka[IAppsService],
    app_service: FromDishka[IAppsService],
    data: EventCreateSchema,
    current_user: CurrentUserDep,
) -> EventResponseSchema:
    event_dto = EventCreateDTO(**data.model_dump(), owner_id=current_user.id)
    event = await event_service.create(event_dto)
    if event is None:
        raise HTTPException(status_code=400, detail="Failed to create event")
    return await to_schema(event, current_user.id, app_service)
    return await to_schema(event, current_user.id, app_service)


@router.get(
    "/",
    summary="Получить список мероприятий",
    response_model=list[EventResponseSchema],
)
async def get_events(
    event_service: FromDishka[IEventService],
    app_service: FromDishka[IAppsService],
    current_user: CurrentUserDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
):
    data = EventGetAllDTO(offset=offset, limit=limit)
    data = EventGetAllDTO(offset=offset, limit=limit)
    events = await event_service.get_event_list(data)
    tasks = [to_schema(event, current_user.id, app_service) for event in events]
    events_response = await asyncio.gather(*tasks)
    return events_response


@router.get(
    "/my/",
    summary="Получить список моих мероприятий",
    response_model=list[EventResponseSchema],
)
async def get_my_events(
    event_service: FromDishka[IEventService],
    movie_service: FromDishka[IAppsService],
    current_user: CurrentUserDep,
) -> list[EventResponseSchema]:
    user_events = await event_service.get_events_by_user_id(user_id=current_user.id)
    tasks = [to_schema(event, current_user.id, movie_service) for event in user_events]
    user_events_response = await asyncio.gather(*tasks)
    return user_events_response


@router.get(
    "/{event_id}",
    summary="Получить данные о мероприятии",
    response_model=EventResponseSchema,
)
async def get_event(
    event_service: FromDishka[IEventService],
    current_user: CurrentUserDep,
    app_service: FromDishka[IAppsService],
    movie_service: FromDishka[IAppsService],
    event_id: str = Path(..., description="ID мероприятия"),
) -> EventResponseSchema:
    event = await event_service.get_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return await to_schema(event, current_user.id, movie_service)


@router.delete("/{event_id}", summary="Удалить мероприятие")
async def delete_event(
    event_service: FromDishka[IEventService],
    current_user: CurrentUserDep,
    event_id: str = Path(..., description="ID мероприятия"),
) -> None:
    try:
        await event_service.delete(event_id, current_user.id)
    except EventNotFoundError:
        raise


@router.patch("/{event_id}", summary="Обновить мероприятие", response_model=EventResponseSchema)
@router.patch("/{event_id}", summary="Обновить мероприятие", response_model=EventResponseSchema)
async def update_event(
    data: EventUpdateSchema,
    event_service: FromDishka[IEventService],
    app_service: FromDishka[IAppsService],
    app_service: FromDishka[IAppsService],
    current_user: CurrentUserDep,
    event_id: str = Path(..., description="ID мероприятия"),
) -> EventResponseSchema:
    event_dto = EventUpdateDTO(id=event_id, **data.model_dump())
    logger.info(f"{event_dto=}")
    updated_event = await event_service.update(event_dto, current_user.id)
    logger.info(f"{updated_event=}")
    if updated_event is None:
        raise HTTPException(status_code=400, detail="Failed to update event")
    return await to_schema(updated_event, current_user.id, app_service)
    return await to_schema(updated_event, current_user.id, app_service)


@router.post(
    "/{event_id}/reserve",
    summary="Забронировать места на мероприятии",
    response_model=ReservationResponseSchema,
)
async def reserve_seats(
    event_service: FromDishka[IEventService],
    current_user: CurrentUserDep,
    reservation_data: ReservationCreateSchema,
) -> ReservationResponseSchema:
    reservation = await event_service.reserve_seats(reservation_data.event_id, current_user.id, reservation_data.seats)
    reservation = await event_service.reserve_seats(reservation_data.event_id, current_user.id, reservation_data.seats)
    created_reservation = ReservationResponseSchema(**reservation.model_dump())
    return created_reservation


@router.post(
    "/nearby/",
    summary="Получить список событий в заданном радиусе от заданной точки",
    response_model=list[EventResponseSchema],
)
@router.post(
    "/nearby/",
    summary="Получить список событий в заданном радиусе от заданной точки",
    response_model=list[EventResponseSchema],
)
async def get_nearby_events(
    event_service: FromDishka[IEventService],
    app_service: FromDishka[IAppsService],
    app_service: FromDishka[IAppsService],
    current_user: CurrentUserDep,
    latitude: float = Query(..., description="Широта"),
    longitude: float = Query(..., description="Долгота"),
    radius: float = Query(3_000.0, description="Радиус в метрах"),
) -> list[EventResponseSchema]:
    events = await event_service.get_nearby_events(latitude, longitude, radius)
    tasks = [to_schema(event, current_user.id, app_service) for event in events]
    event_responses = await asyncio.gather(*tasks)
    tasks = [to_schema(event, current_user.id, app_service) for event in events]
    event_responses = await asyncio.gather(*tasks)
    return event_responses
