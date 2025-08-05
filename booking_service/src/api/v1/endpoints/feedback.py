import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path

from src.api.v1.depends import CurrentUserDep
from src.api.v1.schemas.feedback import (
    FeedbackCreateSchema,
    FeedbackResponseSchema,
)
from src.domain.dtos.feedback import (
    FeedbackCreateDTO,
    FeedbackDeleteDTO,
)
from src.services.feedback import IFeedbackService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/feedback", tags=["Feedback"], route_class=DishkaRoute)


@router.post(
    "/", summary="Поставить оценку", response_model=FeedbackResponseSchema
)
async def create_feedback(
    data: FeedbackCreateSchema,
    feedback_service: FromDishka[IFeedbackService],
    current_user: CurrentUserDep,
):
    feedback_data = FeedbackCreateDTO(**data.model_dump(), user_id=current_user.id)
    return await feedback_service.set_review(feedback=feedback_data)


@router.get(
    "/{event_id}", summary="Получить оценки мероприятия", response_model=list[FeedbackResponseSchema]
)
async def get_feedbacks(
    feedback_service: FromDishka[IFeedbackService],
    event_id: str = Path(..., description="ID ивента"),
):
    return await feedback_service.get(event_id=event_id)


@router.delete("/{event_id}", summary="Убрать оценку")
async def delete_feedback(
    feedback_service: FromDishka[IFeedbackService],
    current_user: CurrentUserDep,
    event_id: str = Path(..., description="ID ивента"),
):
    feedback_data = FeedbackDeleteDTO(event_id=event_id, user_id=current_user.id)")
    return await feedback_service.delete(feedback=feedback_data)
