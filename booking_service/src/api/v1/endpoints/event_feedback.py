import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path

from src.api.v1.depends import CurrentUserDep
from src.api.v1.schemas.event_feedback import (
    EventFeedbackCreateSchema,
    EventFeedbackResponseSchema,
)
from src.domain.dtos.event_feedback import (
    EventFeedbackCreateDTO,
    EventFeedbackDeleteDTO,
)
from src.services.feedback import IEventFeedbackService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/event_feedback", tags=["EventFeedback"], route_class=DishkaRoute)


@router.post(
    "/", summary="Поставить оценку мероприятию", response_model=EventFeedbackResponseSchema
)
async def create_feedback(
    data: EventFeedbackCreateSchema,
    feedback_service: FromDishka[IEventFeedbackService],
    # current_user: CurrentUserDep,
):
    # feedback_data = EventFeedbackCreateDTO(**data.model_dump(), user_id=current_user.id)
    feedback_data = EventFeedbackCreateDTO(**data.model_dump(), user_id="067c88ea-ac1e-7499-8000-dd86f8c118e0")
    return await feedback_service.set_review(feedback=feedback_data)


@router.get(
    "/{event_id}", summary="Получить оценки мероприятия", response_model=list[EventFeedbackResponseSchema]
)
async def get_feedbacks(
    feedback_service: FromDishka[IEventFeedbackService],
    event_id: str = Path(..., description="ID ивента"),
):
    return await feedback_service.get(id=event_id)


@router.delete("/{event_id}", summary="Убрать оценку мероприятию")
async def delete_feedback(
    feedback_service: FromDishka[IEventFeedbackService],
    # current_user: CurrentUserDep,
    event_id: str = Path(..., description="ID ивента"),
):
    # feedback_data = EventFeedbackDeleteDTO(event_id=event_id, user_id=current_user.id)
    feedback_data = EventFeedbackDeleteDTO(event_id=event_id, user_id="067c88ea-ac1e-7499-8000-dd86f8c118e0")
    return await feedback_service.delete(feedback=feedback_data)
