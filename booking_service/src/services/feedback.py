import abc
import datetime
import logging
from uuid import UUID

from src.domain.dtos.event_feedback import (
    EventFeedbackCreateDTO,
    EventFeedbackDeleteDTO,
    EventFeedbackUpdateDTO,
)
from src.domain.dtos.user_feedback import (
    UserFeedbackCreateDTO,
    UserFeedbackDeleteDTO,
    UserFeedbackUpdateDTO,
)
from src.domain.entities.feedback import EventFeedback, UserFeedback
from src.domain.entities.reservation import ReservationStatus
from src.services.exceptions import (
    EventFeedbackNotStartedError,
    EventFeedbackOwnerError,
    FeedbackNotFoundError,
    UserFeedbackSelfError,
    UserFeedbackUserNotFoundError,
)
from src.services.interfaces.uow import IUnitOfWork

logger = logging.getLogger(__name__)


class IBaseFeedbackService(abc.ABC):
    @abc.abstractmethod
    async def set_review(
        self,
        feedback: (
            EventFeedbackCreateDTO
            | EventFeedbackUpdateDTO
            | UserFeedbackCreateDTO
            | UserFeedbackUpdateDTO
        ),
    ) -> EventFeedback: ...

    @abc.abstractmethod
    async def delete(
        self, feedback: EventFeedbackDeleteDTO | UserFeedbackDeleteDTO
    ) -> None: ...

    @abc.abstractmethod
    async def get(self, id: UUID | str) -> list[EventFeedback]: ...


class IEventFeedbackService(IBaseFeedbackService):
    pass


class IUserFeedbackService(IBaseFeedbackService):
    pass


class EventFeedbackService(IEventFeedbackService):
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def set_review(
        self, feedback: EventFeedbackCreateDTO | EventFeedbackUpdateDTO
    ) -> EventFeedback:
        async with self._uow as uow:
            current_event = await uow.event_repository.get_by_id(feedback.event_id)
            if current_event.start_datetime > datetime.datetime.now(datetime.UTC):
                raise EventFeedbackNotStartedError(
                    "Невозможно оставить отзыв на событие, которое еще не началось."
                )
            if current_event.owner_id == feedback.user_id:
                raise EventFeedbackOwnerError(
                    "Невозможно оставить отзыв на свое собственное событие."
                )

            updated_feedback = await uow.event_feedback_repository.update(feedback)
            if updated_feedback is None:
                logger.info(
                    f"Отзыв с {feedback.event_id=}, {feedback.user_id=} не найден. Создаем новый."
                )
                return await uow.event_feedback_repository.create(feedback)
            return updated_feedback

    async def delete(self, feedback: EventFeedbackDeleteDTO) -> None:
        async with self._uow as uow:
            result = await uow.event_feedback_repository.delete(feedback=feedback)
            if not result:
                raise FeedbackNotFoundError(
                    f"Отзыв с {feedback.event_id=}, {feedback.user_id=} не найден."
                )

    async def get(self, id: UUID | str, user_id: UUID) -> list[EventFeedback]:
        async with self._uow as uow:
            all_feedback: dict = await uow.event_feedback_repository.get_id(id=id)
            my_feedback = await uow.event_feedback_repository.get_my_feedback(
                id=id, user_id=user_id
            )
            return (
                all_feedback["positive"],
                all_feedback["negative"],
                getattr(my_feedback, "review", None),
            )


class UserFeedbackService(IUserFeedbackService):
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def set_review(
        self, feedback: UserFeedbackCreateDTO | UserFeedbackUpdateDTO
    ) -> UserFeedback:
        async with self._uow as uow:
            if feedback.owner_id == feedback.user_id:
                raise UserFeedbackSelfError("Невозможно оставить отзыв на самого себя.")

            check = False
            current_events = await uow.event_repository.get_events_by_user_id(
                feedback.owner_id
            )
            for current_event in current_events:
                if check:
                    continue
                if current_event.start_datetime > datetime.datetime.now(datetime.UTC):
                    continue
                for reservation in current_event.reservations:
                    if (
                        reservation.user_id == feedback.user_id
                        and reservation.status == ReservationStatus.SUCCESS
                    ):
                        check = True
                        break
            if not check:
                raise UserFeedbackUserNotFoundError(
                    "Невозможно оставить отзыв, если пользователь не является участником события."
                )

            updated_feedback = await uow.user_feedback_repository.update(feedback)
            if updated_feedback is None:
                logger.info(
                    f"Отзыв с {feedback.owner_id=}, {feedback.user_id=} не найден. Создаем новый."
                )
                return await uow.user_feedback_repository.create(feedback)
            return updated_feedback

    async def delete(self, feedback: UserFeedbackDeleteDTO) -> None:
        async with self._uow as uow:
            result = await uow.user_feedback_repository.delete(feedback=feedback)
            if not result:
                raise FeedbackNotFoundError(
                    f"Отзыв с {feedback.owner_id=}, {feedback.user_id=} не найден."
                )

    async def get(self, id: UUID | str, user_id: UUID) -> list[UserFeedback]:
        async with self._uow as uow:
            all_feedback: dict = await uow.user_feedback_repository.get_id(id=id)
            my_feedback = await uow.user_feedback_repository.get_my_feedback(
                id=id, user_id=user_id
            )
            return (
                all_feedback["positive"],
                all_feedback["negative"],
                getattr(my_feedback, "review", None),
            )

    async def get_events_feedbacks(self, id: UUID | str) -> dict:
        async with self._uow as uow:
            all_feedback: dict = (
                await uow.event_feedback_repository.get_events_feedbacks(id=id)
            )
            logger.info(f"{all_feedback=}")
            return all_feedback["positive"], all_feedback["negative"]
