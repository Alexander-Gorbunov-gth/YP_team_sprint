import abc
import datetime
from uuid import UUID

from src.domain.dtos.feedback import (
    FeedbackCreateDTO,
    FeedbackDeleteDTO,
    FeedbackUpdateDTO,
)
from src.domain.entities.feedback import Feedback
from src.infrastructure.repositories.exceptions import FeedbackNotFoundError
from src.services.exceptions import FeedbackNotStartedError, FeedbackOwnerError
from src.services.interfaces.uow import IUnitOfWork


class IFeedbackService(abc.ABC):
    @abc.abstractmethod
    async def set_review(self, feedback: FeedbackCreateDTO | FeedbackUpdateDTO) -> Feedback: ...

    @abc.abstractmethod
    async def delete(self, feedback: FeedbackDeleteDTO) -> None: ...

    @abc.abstractmethod
    async def get(self, event_id: UUID | str) -> list[Feedback]: ...


class FeedbackService(IFeedbackService):
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def set_review(
        self, feedback: FeedbackCreateDTO | FeedbackUpdateDTO
    ) -> Feedback:
        async with self._uow as uow:
            current_event = await uow.event_repository.get_by_id(feedback.event_id)
            if current_event.start_datetime > datetime.datetime.now(datetime.UTC):
                raise FeedbackNotStartedError(
                    "Невозможно оставить отзыв на событие, которое еще не началось."
                )
            if current_event.owner_id == feedback.user_id:
                raise FeedbackOwnerError(
                    "Невозможно оставить отзыв на свое собственное событие."
                )
            try:
                return await uow.feedback_repository.update(feedback)
            except FeedbackNotFoundError:
                return await uow.feedback_repository.create(feedback)

    async def delete(self, feedback: FeedbackDeleteDTO) -> None:
        async with self._uow as uow:
            await uow.feedback_repository.delete(feedback=feedback)

    async def get(self, event_id: UUID | str) -> list[Feedback]:
        async with self._uow as uow:
            return await uow.feedback_repository.get_id(
                event_id=event_id
            )
