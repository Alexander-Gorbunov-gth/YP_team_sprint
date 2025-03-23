import logging

from fastapi import Depends
from sqlalchemy import Result, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.domain.entities import SocialAccount
from src.domain.exceptions import UserIsExists
from src.domain.repositories import AbstractSocialAccountRepository

logger = logging.getLogger(__name__)


class SQLAlchemySocialAccountRepository(AbstractSocialAccountRepository):
    exclude_fields = ("id", "created_at", "updated_at")

    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def save_social_account(self, social_account: SocialAccount):
        query = (
            insert(SocialAccount)
            .values(social_account.to_dict(self.exclude_fields))
            .returning(SocialAccount)
        )
        try:
            result: Result = await self._session.execute(query)
        except IntegrityError:
            logger.error("Пользователь с user_id/social_name '%s/%s' уже существует.", social_account.user_id, social_account.social_name)
            raise UserIsExists
        await self._session.commit()
        return result.scalar_one()



def get_social_account_repository(session: AsyncSession = Depends(get_session)) -> AbstractSocialAccountRepository:
    session_repository = SQLAlchemySocialAccountRepository(session=session)
    return session_repository
