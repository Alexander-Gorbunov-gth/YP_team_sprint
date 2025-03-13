from uuid import UUID
from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, Result

from src.domain.entities import Session
from src.domain.repositories import AbstractSessionRepository


class SQLAlchemySessionRepository(AbstractSessionRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, session: Session) -> Session:
        query = insert(Session).values(asdict(session)).returning(Session)
        result: Result = await self._session.execute(query)
        return result.scalar_one()

    async def update(self, session: Session) -> Session | None:
        query = (
            update(Session)
            .filter_by(id=session.id)
            .values(asdict(session))
            .returning(Session)
        )
        result: Result = await self._session.execute(query)
        return result.scalar_one()

    async def get_by_refresh_token(self, refresh_token: str) -> Session | None:
        query = select(Session).filter_by(refresh_token=refresh_token)
        result: Result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_sessions_by_user_id(self, user_id: str | UUID) -> list[Session]:
        query = select(Session).filter_by(user_id=user_id)
        result: Result = await self._session.execute(query)
        return result.scalars().all()
