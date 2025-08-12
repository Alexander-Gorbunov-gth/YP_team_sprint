import logging
from uuid import UUID

from sqlalchemy import func, case
from sqlalchemy import Result, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.event import Event
from src.domain.dtos.event_feedback import (
    EventFeedbackCreateDTO,
    EventFeedbackDeleteDTO,
    EventFeedbackUpdateDTO,
)
from src.domain.entities.feedback import EventFeedback
from src.services.interfaces.repositories.feedback import (
    IFeedbackRepository,
    IEventFeedbackRepository,
)

logger = logging.getLogger(__name__)


class SQLAlchemyEventFeedbackRepository(IEventFeedbackRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, feedback: EventFeedbackCreateDTO) -> EventFeedback:
        """
        Создает отзыв в базе данных.
        :param feedback: Схема отзыва для создания.
        :return: Созданный отзыв.
        """

        query = (
            insert(EventFeedback).values(feedback.model_dump()).returning(EventFeedback)
        )
        created_subscription: Result = await self._session.execute(query)
        return created_subscription.scalar_one()

    async def update(self, feedback: EventFeedbackUpdateDTO) -> EventFeedback:
        """
        Обновляет отзыв в базе данных.
        :param feedback: Обновлённый объект отзыва.
        :return: Обновлённый отзыв.
        """

        update_data = feedback.model_dump(
            exclude_unset=True, exclude_defaults=True, exclude={"id"}
        )

        query = (
            update(EventFeedback)
            .where(
                EventFeedback.event_id == feedback.event_id,
                EventFeedback.user_id == feedback.user_id,
            )
            .values(**update_data)
            .returning(EventFeedback)  # type: ignore
        )
        result: Result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, feedback: EventFeedbackDeleteDTO) -> bool:
        """
        Удаляет отзыв из базы данных.
        :param feedback: Схема отзыва для получения.
        """

        check_query = select(EventFeedback).filter_by(
            event_id=feedback.event_id, user_id=feedback.user_id
        )
        result: Result = await self._session.execute(check_query)
        existing = result.scalar_one_or_none()

        if existing is None:
            return False

        await self._session.delete(existing)
        return True

    async def get_id(self, id: UUID | str) -> dict:
        """
        Получает количество позитивных и негативных отзывов события.
        :param id: ID события.
        :return: dict с количеством positive и negative.
        """
        positive_count = func.count(
            case((EventFeedback.review == "positive", 1))
        ).label("positive")
        negative_count = func.count(
            case((EventFeedback.review == "negative", 1))
        ).label("negative")

        query = select(positive_count, negative_count).filter_by(event_id=id)
        result: Result = await self._session.execute(query)
        row = result.one()
        return {"positive": row.positive, "negative": row.negative}

    async def get_my_feedback(self, id: UUID | str, user_id: UUID):
        query = select(EventFeedback).filter_by(event_id=id, user_id=user_id)
        result: Result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_events_feedbacks(self, id: UUID | str) -> dict:
        """
        Получает количество позитивных и негативных отзывов события.
        :param id: ID события.
        :return: dict с количеством positive и negative.
        """
        positive_count = func.count(
            case((EventFeedback.review == "positive", 1))
        ).label("positive")
        negative_count = func.count(
            case((EventFeedback.review == "negative", 1))
        ).label("negative")

        query = (
            select(positive_count, negative_count)
            .join(Event, EventFeedback.event_id == Event.id)
            .where(Event.owner_id == id)
        )

        result: Result = await self._session.execute(query)
        row = result.one()

        return {"positive": row.positive, "negative": row.negative}
