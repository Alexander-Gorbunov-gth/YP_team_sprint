import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path

from src.api.v1.depends import CurrentUserDep
from src.api.v1.schemas.user_feedback import (
    UserFeedbackCreateSchema,
    UserFeedbackResponseSchema,
)
from src.domain.dtos.user_feedback import (
    UserFeedbackCreateDTO,
    UserFeedbackDeleteDTO,
)
from src.services.feedback import IUserFeedbackService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user_feedback", tags=["UserFeedback"], route_class=DishkaRoute)


@router.post(
    "/", summary="Поставить оценку пользователю", response_model=UserFeedbackResponseSchema
)
async def create_feedback(
    data: UserFeedbackCreateSchema,
    feedback_service: FromDishka[IUserFeedbackService],
    # current_user: CurrentUserDep,
):
    # feedback_data = UserFeedbackCreateDTO(**data.model_dump(), owner_id=current_user.id)
    feedback_data = UserFeedbackCreateDTO(**data.model_dump(), owner_id="067c88ea-ac1e-7499-8000-dd86f8c118e0")
    return await feedback_service.set_review(feedback=feedback_data)


@router.get(
    "/{review_user_id}", summary="Получить оценки пользователя", response_model=list[UserFeedbackResponseSchema]
)
async def get_feedbacks(
    feedback_service: FromDishka[IUserFeedbackService],
    review_user_id: str = Path(..., description="ID пользователя"),
):
    return await feedback_service.get(id=review_user_id)


@router.delete("/{review_user_id}", summary="Убрать оценку пользователю")
async def delete_feedback(
    feedback_service: FromDishka[IUserFeedbackService],
    # current_user: CurrentUserDep,
    review_user_id: str = Path(..., description="ID пользователя"),
):
    # feedback_data = UserFeedbackDeleteDTO(user_id=review_user_id, owner_id=current_user.id)
    feedback_data = UserFeedbackDeleteDTO(user_id=review_user_id, owner_id="067c88ea-ac1e-7499-8000-dd86f8c118e0")
    return await feedback_service.delete(feedback=feedback_data)
