from abc import ABC, abstractmethod
from uuid import UUID

from src.infrastructure.models import TemplateModel


class AbstractTemplateRepository(ABC):
    @abstractmethod
    async def get_template(self, template_id: UUID) -> TemplateModel: ...

    @abstractmethod
    async def get_template_by_name(self, name: str) -> TemplateModel: ...
