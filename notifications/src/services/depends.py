from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.container import AppContainer
from src.infrastructure.repositories.template import SQLAlchemyTemplateRepository
from src.services.interfaces.repositories.template import AbstractTemplateRepository

Session_Dep = Annotated[AsyncSession, Depends(AppContainer.get_db_session)]


def get_template_repository(session: Session_Dep) -> AbstractTemplateRepository:
    return SQLAlchemyTemplateRepository(session=session)


Template_Repository_Dep = Annotated[AbstractTemplateRepository, Depends(get_template_repository)]
