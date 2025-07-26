from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.infrastructure.db import postgres
from src.infrastructure.uow import SQLAlchemyUnitOfWork
from src.services.interfaces.uow import IUnitOfWork
from src.services.jwt import AbstractJWTService, JWTService
from src.services.subscription import ISubscriptionService, SubscriptionService


class Container(Provider):
    @provide(scope=Scope.REQUEST)
    async def provide_session(self) -> AsyncIterable[AsyncSession]:
        if postgres.session_maker is None:
            raise RuntimeError("Session maker is not initialized")
        async with postgres.session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_uow(self, session: AsyncSession) -> IUnitOfWork:
        return SQLAlchemyUnitOfWork(session)

    @provide(scope=Scope.REQUEST)
    async def provide_subscription_service(self, uow: IUnitOfWork) -> ISubscriptionService:
        return SubscriptionService(uow)

    @provide(scope=Scope.REQUEST)
    async def provide_jwt_service(self) -> AbstractJWTService:
        return JWTService(settings.auth.secret_key, settings.auth.algorithm)
