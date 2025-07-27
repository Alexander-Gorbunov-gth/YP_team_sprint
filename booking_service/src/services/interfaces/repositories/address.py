import abc
from collections.abc import Iterable
from uuid import UUID

from src.domain.dtos.address import AddressUpdateDTO, AdressCreateDTO
from src.domain.entities.address import Address


class IAddressRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, address: AdressCreateDTO) -> Address: ...

    @abc.abstractmethod
    async def get_address(self, address_id: UUID) -> Address: ...

    @abc.abstractmethod
    async def get_my_addresses(self, user_id: UUID) -> Iterable[Address]: ...

    @abc.abstractmethod
    async def delete(self, address_id: UUID) -> None: ...

    @abc.abstractmethod
    async def update(self, address: AddressUpdateDTO) -> Address: ...
