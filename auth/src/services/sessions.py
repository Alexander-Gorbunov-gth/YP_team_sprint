from fastapi import Depends

from src.domain.entities import Session
from src.domain.interfaces import AbstractSessionService
from src.domain.repositories import AbstractSessionRepository
from src.infrastructure.repositories.sessions import get_session_repository


class SessionService(AbstractSessionService):
    def __init__(self, session_repository: AbstractSessionRepository):
        self._session_repository: AbstractSessionRepository = session_repository

    async def create_new_session(self, session: Session) -> Session:
        new_session = await self._session_repository.create(session)
        return new_session

    async def deactivate_current_session(self, refresh_token: str) -> Session | None:
        current_session = await self._session_repository.get_by_refresh_token(refresh_token)
        current_session.is_active = False
        updated_session = await self._session_repository.update(current_session)
        return updated_session

    async def deactivate_all_without_current(self, refresh_token: str) -> list[Session]:
        current_session = await self._session_repository.get_by_refresh_token(refresh_token)
        user_sessions = await self._session_repository.get_sessions_by_user_id(current_session.user_id)
        deactivate_sessions = []
        for session in user_sessions:
            if session.id != current_session.id:
                session.is_active = False
                await self._session_repository.update(session)
                deactivate_sessions.append(session)
        return deactivate_sessions

    async def update_session_refresh_token(self, old_refresh_token: str, new_refresh_token: str) -> Session | None:
        current_session = await self._session_repository.get_by_refresh_token(old_refresh_token)
        current_session.refresh_token = new_refresh_token
        updated_session = await self._session_repository.update(session=current_session)
        return updated_session


def get_session_service(
    session_repository: AbstractSessionRepository = Depends(get_session_repository),
) -> AbstractSessionService:
    session_service = SessionService(session_repository=session_repository)
    return session_service
