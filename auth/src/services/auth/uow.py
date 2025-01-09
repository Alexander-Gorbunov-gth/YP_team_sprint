from functools import lru_cache

from fastapi import Depends
from src.db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.auth.interfaces import IAuthUoW, ISQLAlchemyUoW
from src.services.auth.repositories import SQLAlchemyAuthRepository
from src.models.users import User
from src.models.permissions import Permission
from src.models.sessions import Session
from src.models.roles import Role


class SQLAlchemyAuthUoW(IAuthUoW, ISQLAlchemyUoW):
    async def __aenter__(self):
        self.users = SQLAlchemyAuthRepository(self._session, User)
        self.sessions = SQLAlchemyAuthRepository(self._session, Session)
        self.roles = SQLAlchemyAuthRepository(self._session, Role)
        self.permissions = SQLAlchemyAuthRepository(self._session, Permission)
        return self


@lru_cache
def get_auth_uow(db_session: AsyncSession = Depends(get_session)) -> IAuthUoW:
    uow = SQLAlchemyAuthUoW(session=db_session)
    return uow
