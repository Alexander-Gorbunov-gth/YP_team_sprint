from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import Settings
from src.models.users import User
from src.services.users.repositories import SqlmodelUserRepository
from src.services.users.services import UserService


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Settings)

    engine = providers.Singleton(
        create_async_engine, url=config.provided.postgres.db_url, echo=config.provided.postgres.db_echo,
    )
    async_session_factory = providers.Singleton(
        sessionmaker, bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async_session = providers.Resource(
        lambda factory: factory(), factory=async_session_factory
    )

    user_repository = providers.Factory(
        SqlmodelUserRepository, session=async_session, model=User
    )

    user_service = providers.Factory(UserService, repository=user_repository)
