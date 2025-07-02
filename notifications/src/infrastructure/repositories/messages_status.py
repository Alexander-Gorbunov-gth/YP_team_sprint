import logging
from datetime import datetime
from uuid import UUID

from fastapi import Depends
from sqlalchemy import Result, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repositories import AbstractMessagesStatusRepository
from src.domain.status import MessageModel, MessageStatus
from src.infrastructure.container import AppContainer

logger = logging.getLogger(__name__)


class SQLAlchemyMessagesStatusRepository(AbstractMessagesStatusRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(
        self,
        body: str,
        sent_to: UUID,
        sent_address: str,
        subject: str,
        status: MessageStatus = MessageStatus.scheduled,
    ) -> MessageModel:
        insert_data = {
            "body": body,
            "sent_to": sent_to,
            "sent_address": sent_address,
            "status": status,
            "subject": subject,
        }
        query = insert(MessageModel).values(insert_data).returning(MessageModel)
        result: Result = await self._session.execute(query)
        await self._commit()
        print("Данные успешно вставлены в таблицу messages_status")
        return result.scalar_one()

    async def update_status(self, id: UUID, status: MessageStatus) -> None:
        await self._session.execute(update(MessageModel).filter_by(id=id).values(status=status))
        await self._commit()

    async def update_send_at(self, id: UUID, send_at: datetime) -> None:
        await self._session.execute(update(MessageModel).filter_by(id=id).values(send_at=send_at))
        await self._commit()

    async def _commit(self) -> None:
        await self._session.commit()


async def get_short_url_repository() -> SQLAlchemyMessagesStatusRepository:
    async with AppContainer.get_db_session() as session:
        if not session:
            raise ValueError("Не удалось получить сессию базы данных")
        return SQLAlchemyMessagesStatusRepository(session=session)
