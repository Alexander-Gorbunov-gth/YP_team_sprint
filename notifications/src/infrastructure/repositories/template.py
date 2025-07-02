import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.models import TemplateModel
from src.infrastructure.repositories.exceptions import TemplateNotFoundError
from src.services.interfaces.repositories.template import AbstractTemplateRepository

logger = logging.getLogger(__name__)


class SQLAlchemyTemplateRepository(AbstractTemplateRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_template(self, template_id: UUID) -> TemplateModel:
        query = select(TemplateModel).where(TemplateModel.id == template_id)
        result: Result[TemplateModel, None] = await self.session.execute(query)
        if template := result.scalar_one_or_none():
            return template
        logger.error("Шаблон с id %s не найден", template_id)
        raise TemplateNotFoundError(f"Шаблон с id {template_id} не найден")

    async def get_template_by_name(self, name: str) -> TemplateModel:
        query = select(TemplateModel).where(TemplateModel.name == name)
        result: Result[TemplateModel, None] = await self.session.execute(query)
        if template := result.scalar_one_or_none():
            return template
        logger.error("Шаблон с именем %s не найден", name)
        raise TemplateNotFoundError(f"Шаблон с именем {name} не найден")
