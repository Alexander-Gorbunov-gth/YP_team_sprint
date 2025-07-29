from collections.abc import Iterable
from uuid import UUID

from src.domain.dtos.address import AddressCreateDTO, AddressUpdateDTO
from src.domain.entities.address import Address
from src.services.interfaces.repositories.address import IAddressRepository


class FakeAddressRepository(IAddressRepository):
    def __init__(self) -> None:
        self._addresses: list[Address] = []

    async def create(self, address: AddressCreateDTO) -> Address:
        created_address = Address.create(**address.model_dump())
        self._addresses.append(created_address)
        return created_address

    async def get_address(self, address_id: UUID) -> Address | None:
        for address in self._addresses:
            if address.id == address_id:
                return address
        return None

    async def get_my_addresses(self, user_id: UUID) -> Iterable[Address]:
        return [address for address in self._addresses if address.user_id == user_id]

    async def delete(self, address_id: UUID) -> Address | None:
        for address in self._addresses:
            if address.id == address_id:
                self._addresses.remove(address)
                return address
        return None

    async def update(self, address: AddressUpdateDTO) -> Address | None:
        insert_data = address.model_dump(exclude_unset=True)
        if not insert_data:
            return None
        for i, a in enumerate(self._addresses):
            if a.id == address.id:
                for key, value in insert_data.items():
                    setattr(self._addresses[i], key, value)
                return self._addresses[i]
        return None
