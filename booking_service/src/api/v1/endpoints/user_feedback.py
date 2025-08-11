import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path

from src.api.v1.depends import CurrentUserDep
from src.api.v1.schemas.user_feedback import (
    UserFeedbackCreateSchema,
    UserFeedbackResponseSchema,
    ResultFeedbackResponseSchema,
    ResultUserEventFeedbackResponseSchema,
)
from src.domain.dtos.user_feedback import (
    UserFeedbackCreateDTO,
    UserFeedbackDeleteDTO,
)
from src.services.feedback import IUserFeedbackService, IEventFeedbackService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user-feedback", tags=["UserFeedback"], route_class=DishkaRoute
)


@router.post(
    "/",
    summary="Поставить оценку пользователю",
    response_model=UserFeedbackResponseSchema,
)
async def create_feedback(
    data: UserFeedbackCreateSchema,
    feedback_service: FromDishka[IUserFeedbackService],
    current_user: CurrentUserDep,
):
    feedback_data = UserFeedbackCreateDTO(**data.model_dump(), owner_id=current_user.id)
    return await feedback_service.set_review(feedback=feedback_data)


@router.get(
    "/{review_user_id}",
    summary="Получить оценки пользователя",
    response_model=ResultFeedbackResponseSchema,
)
async def get_feedbacks(
    feedback_service: FromDishka[IUserFeedbackService],
    current_user: CurrentUserDep,
    review_user_id: str = Path(..., description="ID пользователя"),
):
    user_id = current_user.id
    positive, negative, my_feedback = await feedback_service.get(
        id=review_user_id, user_id=user_id
    )
    return ResultFeedbackResponseSchema(
        user_id=review_user_id, my=my_feedback, positive=positive, negative=negative
    )


@router.delete("/{review_user_id}", summary="Убрать оценку пользователю")
async def delete_feedback(
    feedback_service: FromDishka[IUserFeedbackService],
    current_user: CurrentUserDep,
    review_user_id: str = Path(..., description="ID пользователя"),
):
    feedback_data = UserFeedbackDeleteDTO(
        user_id=review_user_id, owner_id=current_user.id
    )
    return await feedback_service.delete(feedback=feedback_data)


@router.get(
    "/events/{review_user_id}",
    summary="Получить оценки событий пользователя",
    response_model=ResultFeedbackResponseSchema,
)
async def get_events_feedbacks(
    feedback_service: FromDishka[IUserFeedbackService],
    current_user: CurrentUserDep,
    review_user_id: str = Path(..., description="ID пользователя"),
):
    positive, negative = await feedback_service.get_events_feedbacks(id=review_user_id)
    logger.info(f"{positive=}, {negative=}")
    return ResultUserEventFeedbackResponseSchema(
        user_id=review_user_id, positive=positive, negative=negative
    )
