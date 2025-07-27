import logging

from fastapi import APIRouter

from src.api.v1.schemas.event import EventCreateSchema, EventResponseSchema, EventUpdateSchema
from tests.unit.routers_fixture import event_data, event_my_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", summary="Создать мероприятие", response_model=EventResponseSchema)
async def create_event(
    data: EventCreateSchema,
):
    return event_data


@router.get(
    "/",
    summary="Получить список мероприятий",
    response_model=list[EventResponseSchema],
)
async def get_events():
    return [event_data]


@router.get(
    "/my/",
    summary="Получить список моих мероприятий",
    response_model=list[EventResponseSchema],
)
async def get_my_events():
    return [event_my_data]


@router.get(
    "/{id}",
    summary="Получить данные о мероприятии",
    response_model=EventResponseSchema,
)
async def get_event():
    return event_data


@router.delete("/{id}", summary="Удалить мероприятие")
async def delete_event() -> bool:
    return True


@router.patch("/{id}", summary="Обновить мероприятие", response_model=EventResponseSchema)
async def update_event(data: EventUpdateSchema):
    return event_data
