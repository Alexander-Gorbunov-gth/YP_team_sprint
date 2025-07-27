import logging
from uuid import UUID

from fastapi import Depends
from sqlalchemy import Result, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_session
from src.domain.entities.address import Address
from src.api.v1.schemas.address import UpdateAddressSchema
from src.services.interfaces.repositories.address import IAddressRepository

logger = logging.getLogger(__name__)


class SQLAlchemyAddressRepository(IAddressRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(
        self,
        user_id: UUID,
        latitude: float,
        longitude: float,
        country: str,
        city: str,
        street: str,
        house: str,
        flat: str | None = None,
        # TODO: Применить схему AdressCreateSchema
    ) -> Address:
        insert_data = {
            "user_id": user_id,
            "latitude": latitude,
            "longitude": longitude,
            "country": country,
            "city": city,
            "street": street,
            "house": house,
            "flat": flat,
        }

        query = insert(Address).values(insert_data).returning(Address)
        result: Result = await self._session.execute(query)
        await self._commit()
        return result.scalar_one()

    async def get_address(self, address_id: UUID) -> Address | None:
        query = select(Address).filter_by(id=address_id)
        result: Result = await self._session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_my_address(self, user_id: UUID) -> list[Address]:
        query = select(Address).filter_by(user_id=user_id)
        result: Result = await self._session.execute(query)
        return result.unique().scalars().all()

    async def delete(self, address_id: UUID) -> Address | None:
        query = select(Address).filter_by(id=address_id)
        result: Result = await self._session.execute(query)
        address = result.scalar_one_or_none()

        if address is None:
            logger.warning(f"Удаляемый Address с id={address_id} не найден.")
            return None

        await self._session.delete(address)
        await self._commit()
        return address

    async def update(self, address_id: UUID, address: UpdateAddressSchema) -> Address:
        update_data = address.model_dump(exclude_unset=True)

        if not update_data:
            return None

        stmt = (
            update(Address)
            .where(Address.id == address_id)
            .values(**update_data)
            .returning(Address)
        )
        result: Result = await self._session.execute(stmt)
        updated_address = result.scalar_one_or_none()

        if updated_address is None:
            logger.warning(f"Address с id={address_id} не найден для обновления.")
            return None

        await self._commit()
        return updated_address

    async def _commit(self) -> None:
        await self._session.commit()


async def get_address_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyAddressRepository:
    return SQLAlchemyAddressRepository(session=session)
