from uuid import UUID

from domain.templates import Template
from src.services.interfaces.services.template import AbstractTemplateService
from src.services.interfaces.repositories.template import AbstractTemplateRepository

class TemplateService(AbstractTemplateService):
    def __init__(self, template_repository: AbstractTemplateRepository):
        self._template_repository = template_repository

    async def get_template(self, template_id: UUID) -> Template:
        template = await self._template_repository.get_template(template_id=template_id)
        return Template(
            id=template.id,
            name=template.name,
            description=template.description,
            created_at=template.created_at,
            updated_at=template.updated_at,
        )
    
class Template(BaseModel):
    id: UUID
    channel: ChannelTypes
    event_type: str
    subject: str | None
    body: str