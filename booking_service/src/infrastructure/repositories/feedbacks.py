import logging
from uuid import UUID

from sqlalchemy import Result, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.dtos.feedback import (
    FeedbackCreateDTO,
    FeedbackDeleteDTO,
    FeedbackUpdateDTO,
)
from src.domain.entities.feedback import Feedback
from src.infrastructure.repositories.exceptions import FeedbackNotFoundError, NotModifiedError
from src.services.interfaces.repositories.feedback import IFeedbackRepository

logger = logging.getLogger(__name__)


class SQLAlchemyFeedbackRepository(IFeedbackRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(
        self,
        feedback: FeedbackCreateDTO
    ) -> Feedback:
        """
        Создает отзыв в базе данных.
        :param feedback: Схема отзыва для создания.
        :return: Созданный отзыв.
        """

        query = (
            insert(Feedback).values(feedback.model_dump()).returning(Feedback)
        )
        created_subscription: Result = await self._session.execute(query)
        await self._commit()
        return created_subscription.scalar_one()

    async def update(
        self,
        feedback: FeedbackUpdateDTO
    ) -> Feedback:
        """
        Обновляет отзыв в базе данных.
        :param feedback: Обновлённый объект отзыва.
        :return: Обновлённый отзыв.
        :raises FeedbackNotFoundError: Если отзыв не найден.
        """

        update_data = feedback.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude={"id"}
        )
        if not update_data:
            raise NotModifiedError("Не указаны данные для обновления.")

        query = (
            update(Feedback)
            .where(
                Feedback.event_id == feedback.event_id,
                Feedback.user_id == feedback.user_id
            )
            .values(**update_data)
            .returning(Feedback)  # type: ignore
        )
        result: Result = await self._session.execute(query)
        updated_feedback = result.scalar_one_or_none()

        if updated_feedback is None:
            raise FeedbackNotFoundError(
                f"Отзыв с {feedback.event_id=}, {feedback.event_id=} не найден."
            )

        return updated_feedback

    async def delete(
        self,
        feedback: FeedbackDeleteDTO
    ) -> None:
        """
        Удаляет отзыв из базы данных.
        :param feedback: Схема отзыва для получения.
        :raises FeedbackNotFoundError: Если отзыв не найден.
        """

        check_query = select(Feedback).filter_by(
            event_id=feedback.event_id,
            user_id=feedback.user_id
        )
        result: Result = await self._session.execute(check_query)
        existing = result.scalar_one_or_none()

        if existing is None:
            raise FeedbackNotFoundError(
                f"Отзыв с {feedback.event_id=}, {feedback.event_id=} не найден."
            )

        await self._session.delete(existing)
        await self._commit()

    async def get_id(
        self,
        event_id: UUID | str
    ) -> list[Feedback]:
        """
        Получает все отзывы события.
        :param event_id: ID события.
        :return: Список отзывов.
        """

        query = (
            select(Feedback)
            .filter_by(event_id=event_id)
            .order_by(Feedback.created_at.desc())
        )
        result: Result = await self._session.execute(query)
        return result.scalars().all()

    async def _commit(self) -> None:
        await self._session.commit()
