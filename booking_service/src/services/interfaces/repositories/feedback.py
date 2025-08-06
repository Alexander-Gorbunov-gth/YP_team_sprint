import abc
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
from src.domain.entities.feedback import EventFeedback


class IFeedbackRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, feedback: EventFeedbackCreateDTO | UserFeedbackCreateDTO) -> EventFeedback: ...

    @abc.abstractmethod
    async def update(self, feedback: EventFeedbackUpdateDTO | UserFeedbackUpdateDTO) -> EventFeedback: ...

    @abc.abstractmethod
    async def delete(self, feedback: EventFeedbackDeleteDTO | UserFeedbackDeleteDTO) -> bool: ...

    @abc.abstractmethod
    async def get_id(self, id: UUID | str) -> list[EventFeedback]: ...
