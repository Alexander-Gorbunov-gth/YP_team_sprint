from src.domain.entities import Session
from src.domain.interfaces import AbstractSessionService


class SessionService(AbstractSessionService):
    def __init__(self, session_repository):
        self._session_repository = session_repository

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
        others_session = await self._session_repository.get_other_sessions_by_user_id(current_session.user_id, current_session)
        for session in others_session:
            session.is_active = False
        return others_session

