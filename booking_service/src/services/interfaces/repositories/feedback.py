import abc
from uuid import UUID

from src.domain.dtos.feedback import (
    FeedbackCreateDTO,
    FeedbackDeleteDTO,
    FeedbackUpdateDTO,
)
from src.domain.entities.feedback import Feedback


class IFeedbackRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, feedback: FeedbackCreateDTO) -> Feedback: ...

    @abc.abstractmethod
    async def update(self, feedback: FeedbackUpdateDTO) -> Feedback: ...

    @abc.abstractmethod
    async def delete(self, feedback: FeedbackDeleteDTO) -> None: ...

    @abc.abstractmethod
    async def get_id(self, event_id: UUID | str) -> list[Feedback]: ...
