from uuid import UUID, uuid4

from src.domain.entities import Session, User
from src.domain.exceptions import UserIsExists
from src.domain.repositories import AbstractSessionRepository, AbstractUserRepository


class FakeUserRepository(AbstractUserRepository):
    """Фейковый репозиторий для пользователей"""

    def __init__(self):
        self._users = {}

    async def create(self, email: str, password: str) -> User:
        if email in self._users:
            raise UserIsExists
        user = User(id="test-user-id", email=email, password=password, is_active=False)
        self._users[email] = user
        return user

    async def get_by_email(self, email: str) -> User | None:
        return self._users.get(email)

    async def get_by_id(self, user_id) -> User | None:
        return next((user for user in self._users.values() if user.id == user_id), None)

    async def update(self, user: User) -> User:
        self._users[user.email] = user
        return user


class FakeSessionRepository(AbstractSessionRepository):
    """Фейковый репозиторий для сессий"""

    def __init__(self):
        self._sessions: dict[str, Session] = {}

    async def create(self, session: Session) -> Session:
        session.id = session.id or uuid4()
        self._sessions[session.id] = session
        return session

    async def update(self, session: Session) -> Session | None:
        if session.id not in self._sessions:
            raise ValueError()

        self._sessions[session.id] = session
        return session

    async def get_by_refresh_token(self, refresh_token: str) -> Session | None:
        return next(
            (session for session in self._sessions.values() if session.refresh_token == refresh_token),
            None,
        )

    async def get_sessions_by_user_id(self, user_id: str | UUID) -> list[Session]:
        user_sessions = [session for session in self._sessions.values() if session.user_id == user_id]
        return user_sessions
