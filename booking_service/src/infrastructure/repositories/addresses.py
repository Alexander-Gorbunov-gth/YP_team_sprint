import logging
from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import Result, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.dtos.address import AddressUpdateDTO, AdressCreateDTO
from src.domain.entities.address import Address
from src.infrastructure.repositories.exceptions import AddressNotFoundError, NotModifiedError
from src.services.interfaces.repositories.address import IAddressRepository

logger = logging.getLogger(__name__)


class SQLAlchemyAddressRepository(IAddressRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, address: AdressCreateDTO) -> Address:
        query = insert(Address).values(address.model_dump()).returning(Address)
        result: Result = await self._session.execute(query)
        return result.scalar_one()

    async def get_address(self, address_id: UUID) -> Address:
        query = select(Address).filter_by(id=address_id)
        result: Result = await self._session.execute(query)
        address = result.scalar_one_or_none()
        if address is None:
            logger.warning("Address с id=%s не найден.", address_id)
            raise AddressNotFoundError(f"Address с id={address_id} не найден.")
        return address

    async def get_my_addresses(self, user_id: UUID) -> Iterable[Address]:
        query = select(Address).filter_by(user_id=user_id)
        result: Result = await self._session.execute(query)
        return result.unique().scalars().all()

    async def delete(self, address_id: UUID) -> None:
        query = select(Address).filter_by(id=address_id)
        result: Result = await self._session.execute(query)
        address = result.scalar_one_or_none()
        if address is None:
            logger.warning("Удаляемый Address с id=%s не найден.", address_id)
            raise AddressNotFoundError(f"Address с id={address_id} не найден.")

        await self._session.delete(address)
        return

    async def update(self, address: AddressUpdateDTO) -> Address:
        update_data = address.model_dump(exclude_unset=True)
        if not update_data:
            raise NotModifiedError("Не указаны данные для обновления.")

        query = update(Address).where(Address.id == address.id).values(**update_data).returning(Address)  # type: ignore
        result: Result = await self._session.execute(query)
        updated_address = result.scalar_one_or_none()

        if updated_address is None:
            logger.warning("Address с id=%s не найден для обновления.", address.id)
            raise AddressNotFoundError(f"Address с id={address.id} не найден для обновления.")

        return updated_address
