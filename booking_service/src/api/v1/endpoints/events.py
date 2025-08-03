import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException, Path

from src.services.event import IEventService
from src.api.v1.depends import CurrentUserDep
from src.domain.dtos.event import EventCreateDTO, EventGetAllDTO, EventUpdateDTO
from src.api.v1.schemas.utils import Author, MovieSchema
from src.api.v1.schemas.event import EventCreateSchema, EventGetAllSchema, EventResponseSchema, EventUpdateSchema
from src.services.event import IEventService
from src.infrastructure.handlers.exceptions import EventNotFoundError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"], route_class=DishkaRoute)


@router.post("/", summary="Создать мероприятие", response_model=EventResponseSchema)
async def create_event(
    event_service: FromDishka[IEventService],
    data: EventCreateSchema,
    current_user: CurrentUserDep
) -> EventResponseSchema:
    event_dto = EventCreateDTO(**data.model_dump(), owner_id=current_user.id)
    event = await event_service.create(event_dto)
    if event is None:
        raise HTTPException(status_code=400, detail="Failed to create event")
    author = Author(id=event.owner_id)
    movie = MovieSchema(id=event.movie_id)
    event_response = EventResponseSchema(**event.model_dump(exclude={"address"}), author=author, movie=movie, address=event.get_address_for_user(user_id=current_user.id))
    return event_response


@router.get(
    "/",
    summary="Получить список мероприятий",
    response_model=list[EventResponseSchema],
)
async def get_events(
    event_service: FromDishka[IEventService],
    data: EventGetAllSchema,
):
    return await event_service.get_event_list(data)


@router.get(
    "/my/",
    summary="Получить список моих мероприятий",
    response_model=list[EventResponseSchema],
)
async def get_my_events(
    event_service: FromDishka[IEventService],
    current_user: CurrentUserDep,
) -> list[EventResponseSchema]:
    user_events = await event_service.get_events_by_user_id(user_id=current_user.id)
    user_events_response = []
    for user_event in user_events:
        author = Author(id=user_event.owner_id)
        movie = MovieSchema(id=user_event.movie_id)
        event_response = EventResponseSchema(**user_event.model_dump(exclude={"address"}), author=author, movie=movie, address=user_event.get_address_for_user(user_id=current_user.id))
        user_events_response.append(event_response)
    return user_events_response


@router.get(
    "/{event_id}",
    summary="Получить данные о мероприятии",
    response_model=EventResponseSchema,
)
async def get_event(
    event_service: FromDishka[IEventService],
    current_user: CurrentUserDep,
    event_id: str = Path(..., description="ID мероприятия"),
) -> EventResponseSchema:
    event = await event_service.get_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    author = Author(id=event.owner_id)
    movie = MovieSchema(id=event.movie_id)
    event_response = EventResponseSchema(**event.model_dump(exclude={"address"}), author=author, movie=movie, address=event.get_address_for_user(user_id=current_user.id))
    return event_response


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


@router.patch("/{id}", summary="Обновить мероприятие", response_model=EventResponseSchema)
async def update_event(
    data: EventUpdateSchema,
    event_service: FromDishka[IEventService],
    current_user: CurrentUserDep,
) -> EventResponseSchema:
    event_dto = EventUpdateDTO(**data.model_dump())
    updated_event = await event_service.update(event_dto, current_user.id)
    if updated_event is None:
        raise HTTPException(status_code=400, detail="Failed to update event")
    author = Author(id=updated_event.owner_id)
    movie = MovieSchema(id=updated_event.movie_id)
    event_response = EventResponseSchema(**updated_event.model_dump(exclude={"address"}), author=author, movie=movie, address=updated_event.get_address_for_user(user_id=current_user.id))
    return event_response

