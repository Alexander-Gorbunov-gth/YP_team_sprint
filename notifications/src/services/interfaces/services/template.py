from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.templates import Template


class AbstractTemplateService(ABC):
    @abstractmethod
    async def get_template(self, template_id: UUID) -> Template: ...

    @abstractmethod
    async def get_template_by_name(self, name: str) -> Template: ...

    @abstractmethod
    async def preview_template(self, template_id: UUID) -> str: ...
