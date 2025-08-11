import logging
from uuid import UUID

from sqlalchemy import Result, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, case

from src.domain.dtos.user_feedback import (
    UserFeedbackCreateDTO,
    UserFeedbackDeleteDTO,
    UserFeedbackUpdateDTO,
)
from src.domain.entities.feedback import UserFeedback
from src.services.interfaces.repositories.feedback import IFeedbackRepository

logger = logging.getLogger(__name__)


class SQLAlchemyUserFeedbackRepository(IFeedbackRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, feedback: UserFeedbackCreateDTO) -> UserFeedback:
        """
        Создает отзыв в базе данных.
        :param feedback: Схема отзыва для создания.
        :return: Созданный отзыв.
        """

        query = (
            insert(UserFeedback).values(feedback.model_dump()).returning(UserFeedback)
        )
        created_subscription: Result = await self._session.execute(query)
        return created_subscription.scalar_one()

    async def update(self, feedback: UserFeedbackUpdateDTO) -> UserFeedback:
        """
        Обновляет отзыв в базе данных.
        :param feedback: Обновлённый объект отзыва.
        :return: Обновлённый отзыв.
        """

        update_data = feedback.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude={"id"}
        )

        query = (
            update(UserFeedback)
            .where(
                UserFeedback.owner_id == feedback.owner_id,
                UserFeedback.user_id == feedback.user_id,
            )
            .values(**update_data)
            .returning(UserFeedback)  # type: ignore
        )
        result: Result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, feedback: UserFeedbackDeleteDTO) -> bool:
        """
        Удаляет отзыв из базы данных.
        :param feedback: Схема отзыва для получения.
        """

        check_query = select(UserFeedback).filter_by(
            owner_id=feedback.owner_id, user_id=feedback.user_id
        )
        result: Result = await self._session.execute(check_query)
        existing = result.scalar_one_or_none()

        if existing is None:
            return False

        await self._session.delete(existing)
        return True

    async def get_id(self, id: UUID | str) -> list[UserFeedback]:
        """
        Получает количество позитивных и негативных отзывов пользователя.
        :param id: ID пользователя.
        :return: dict с количеством positive и negative.
        """
        positive_count = func.count(case((UserFeedback.review == "positive", 1))).label(
            "positive"
        )
        negative_count = func.count(case((UserFeedback.review == "negative", 1))).label(
            "negative"
        )

        query = select(positive_count, negative_count).filter_by(user_id=id)
        result: Result = await self._session.execute(query)
        row = result.one()
        return {"positive": row.positive, "negative": row.negative}

    async def get_my_feedback(self, id: UUID | str, user_id: UUID):
        query = select(UserFeedback).filter_by(user_id=id, owner_id=user_id)
        result: Result = await self._session.execute(query)
        return result.scalar_one_or_none()
