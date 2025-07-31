import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path

from src.api.v1.depends import CurrentUserDep
from src.api.v1.schemas.event import EventCreateSchema, EventGetAllSchema, EventResponseSchema, EventUpdateSchema
from src.services.event import IEventService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"], route_class=DishkaRoute)


@router.post("/", summary="Создать мероприятие", response_model=EventResponseSchema)
async def create_event(
    event_service: FromDishka[IEventService],
    data: EventCreateSchema,
):
    return await event_service.create(data)


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
    user: CurrentUserDep,
    event_service: FromDishka[IEventService],
):
    return await event_service.get_events_by_user_id(user.id)


@router.get(
    "/{id}",
    summary="Получить данные о мероприятии",
    response_model=EventResponseSchema,
)
async def get_event(
    event_service: FromDishka[IEventService],
    id: str = Path(..., description="ID мероприятия"),
):
    return await event_service.get_by_id(id)


@router.delete("/{id}", summary="Удалить мероприятие")
async def delete_event(
    event_service: FromDishka[IEventService],
    id: str = Path(..., description="ID мероприятия"),
) -> bool:
    return await event_service.delete(id)


@router.patch("/{id}", summary="Обновить мероприятие", response_model=EventResponseSchema)
async def update_event(
    data: EventUpdateSchema,
    event_service: FromDishka[IEventService],
):
    return await event_service.update(data)
