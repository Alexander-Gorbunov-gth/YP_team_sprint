import abc
from uuid import UUID

from src.domain.entities.address import Address
from src.domain.schemas.address import AdressCreateSchema, UpdateAddressSchema


class IAddressRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, address: AdressCreateSchema) -> Address:
        pass

    @abc.abstractmethod
    async def get_address(self, address_id: UUID) -> Address:
        pass

    @abc.abstractmethod
    async def get_my_address(self, user_id: UUID) -> list[Address]:
        pass

    @abc.abstractmethod
    async def delete(self, address_id: UUID) -> bool:
        pass

    @abc.abstractmethod
    async def update(self, address_id: UUID, address: UpdateAddressSchema) -> Address:
        pass
