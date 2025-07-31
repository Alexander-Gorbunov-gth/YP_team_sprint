import pytest

from src.domain.dtos.address import AddressCreateDTO, AddressUpdateDTO
from src.services.address import AddressService, IAddressService
from src.services.exceptions import AddressNotFoundError
from tests.fakes.uow import FakeUnitOfWork
from tests.unit.factories import AddressCreateDTOFactory, AddressUpdateDTOFactory


@pytest.fixture
def uow() -> FakeUnitOfWork:
    return FakeUnitOfWork()


@pytest.fixture
def address_service(uow: FakeUnitOfWork) -> IAddressService:
    return AddressService(uow=uow)


@pytest.fixture
def address_create_dto() -> AddressCreateDTO:
    return AddressCreateDTOFactory.build()


@pytest.fixture
def address_update_dto() -> AddressUpdateDTO:
    return AddressUpdateDTOFactory.build()


@pytest.mark.asyncio
async def test_create_update_and_delete_address(
    address_service: IAddressService, address_create_dto: AddressCreateDTO, address_update_dto: AddressUpdateDTO
):
    address = await address_service.create_address(address=address_create_dto)
    assert address is not None
    assert address.latitude == address_create_dto.latitude
    assert address.longitude == address_create_dto.longitude

    address_update_dto.id = address.id
    updated_address = await address_service.update_address(address=address_update_dto)
    assert updated_address is not None
    assert updated_address.latitude == address_update_dto.latitude
    assert updated_address.longitude == address_update_dto.longitude

    deleted_address = await address_service.delete_address(address_id=address.id)
    assert deleted_address is not None
    assert deleted_address.id == address.id


@pytest.mark.asyncio
async def test_get_address_by_id(address_service: IAddressService, address_create_dto: AddressCreateDTO):
    address = await address_service.create_address(address=address_create_dto)
    created_address = await address_service.get_address_by_id(address_id=address.id)

    assert created_address is not None
    assert created_address.id == address.id
    assert created_address.latitude == address.latitude
    assert created_address.longitude == address.longitude


@pytest.mark.asyncio
async def test_get_my_addresses(address_service: IAddressService, address_create_dto: AddressCreateDTO):
    address = await address_service.create_address(address=address_create_dto)
    created_address = list(await address_service.get_my_addresses(user_id=address.user_id))

    assert len(created_address) == 1
    assert created_address[0].id == address.id
    assert created_address[0].latitude == address.latitude
    assert created_address[0].longitude == address.longitude


@pytest.mark.asyncio
async def test_get_my_addresses_empty(address_service: IAddressService, address_create_dto: AddressCreateDTO):
    created_address = list(await address_service.get_my_addresses(user_id=address_create_dto.user_id))

    assert len(created_address) == 0


@pytest.mark.asyncio
async def test_get_address_by_id_not_found(address_service: IAddressService, address_update_dto: AddressUpdateDTO):
    with pytest.raises(AddressNotFoundError):
        await address_service.get_address_by_id(address_id=address_update_dto.id)


@pytest.mark.asyncio
async def test_update_address_not_found(address_service: IAddressService, address_update_dto: AddressUpdateDTO):
    with pytest.raises(AddressNotFoundError):
        await address_service.update_address(address=address_update_dto)


@pytest.mark.asyncio
async def test_delete_address_not_found(address_service: IAddressService, address_update_dto: AddressUpdateDTO):
    with pytest.raises(AddressNotFoundError):
        await address_service.delete_address(address_id=address_update_dto.id)
