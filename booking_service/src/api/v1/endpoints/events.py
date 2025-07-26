import logging

from fastapi import APIRouter

from src.domain.schemas import event as schema
from tests.unit.routers_fixture import event_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", summary="Создать мероприятие", response_model=schema.EventResponseSchema)
async def create_event(
    data: schema.EventCreateSchema,
):
    return event_data


@router.get("/", summary="Получить список мероприятий", response_model=list[schema.EventResponseSchema])
async def get_events():
    return [event_data, event_data, event_data]


@router.get("/{id}", summary="Получить данные о мероприятии", response_model=schema.EventResponseSchema)
async def get_event():
    return event_data


@router.delete("/{id}", summary="Удалить мероприятие")
async def delete_event() -> bool:
    return True


@router.patch("/{id}", summary="Обновить мероприятие", response_model=schema.EventResponseSchema)
async def update_event(data: schema.EventUpdateSchema):
    return event_data
