from collections.abc import Iterable
from uuid import UUID

from src.domain.dtos.address import AddressUpdateDTO, AdressCreateDTO
from src.domain.entities.address import Address
from src.infrastructure.repositories.exceptions import AddressNotFoundError, NotModifiedError
from src.services.interfaces.repositories.address import IAddressRepository


class FakeAddressRepository(IAddressRepository):
    def __init__(self) -> None:
        self._addresses: list[Address] = []

    async def create(self, address: AdressCreateDTO) -> Address:
        created_address = Address.create(**address.model_dump())
        self._addresses.append(created_address)
        return created_address

    async def get_address(self, address_id: UUID) -> Address:
        for address in self._addresses:
            if address.id == address_id:
                return address
        raise AddressNotFoundError(f"Address с id={address_id} не найден.")

    async def get_my_addresses(self, user_id: UUID) -> Iterable[Address]:
        return [address for address in self._addresses if address.user_id == user_id]

    async def delete(self, address_id: UUID) -> None:
        self._addresses = [address for address in self._addresses if address.id != address_id]

    async def update(self, address: AddressUpdateDTO) -> Address:
        insert_data = address.model_dump(exclude_unset=True)
        if not insert_data:
            raise NotModifiedError("Не указаны данные для обновления.")
        for i, a in enumerate(self._addresses):
            if a.id == address.id:
                self._addresses[i] = Address.create(**address.model_dump())
                return self._addresses[i]
        raise AddressNotFoundError(f"Address с id={address.id} не найден.")
