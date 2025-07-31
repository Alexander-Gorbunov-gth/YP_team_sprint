import logging
from uuid import UUID

from fastapi import APIRouter
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.api.v1.schemas.address import AddressCreateSchema, AddressResponseSchema, UpdateAddressSchema
from src.api.v1.depends import CurrentUserDep
from src.services.address import IAddressService
from src.domain.dtos.address import AddressCreateDTO, AddressUpdateDTO

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/address", tags=["Address"], route_class=DishkaRoute)


@router.post("/", summary="Создать адрес", response_model=AddressResponseSchema)
async def create_address(address_data: AddressCreateSchema, user: CurrentUserDep, address_service: FromDishka[IAddressService]):
    address_dto = AddressCreateDTO(**address_data.model_dump(), user_id=user.id)
    address = await address_service.create_address(address_dto)
    return AddressResponseSchema(**address.model_dump())


@router.get(
    "/{address_id}",
    summary="Получить данные об адресе",
    response_model=AddressResponseSchema,
)
async def get_address(address_service: FromDishka[IAddressService], address_id: UUID, user: CurrentUserDep):
    address = await address_service.get_address_by_id(address_id=address_id, user_id=user.id)
    return AddressResponseSchema(**address.model_dump())


@router.get(
    "/my/",
    summary="Получить список моих адресов",
    response_model=list[AddressResponseSchema],
)
async def get_my_address(address_service: FromDishka[IAddressService], user: CurrentUserDep):
    address_data = await address_service.get_my_addresses(user.id)
    return [AddressResponseSchema(**address.model_dump()) for address in address_data]


@router.delete("/{address_id}", summary="Удалить адрес")
async def delete_address(address_service: FromDishka[IAddressService], user: CurrentUserDep, address_id: UUID) -> bool:
    await address_service.delete_address(address_id=address_id, user_id=user.id)
    return True


@router.patch("/{address_id}", summary="Изменить адрес", response_model=AddressResponseSchema)
async def update_address(data: UpdateAddressSchema, user: CurrentUserDep, address_service: FromDishka[IAddressService], address_id: UUID):
    address_dto = AddressUpdateDTO(**data.model_dump(), user_id=user.id, id=address_id)
    address = await address_service.update_address(address_dto, user_id=user.id, address_id=address_id)
    return AddressResponseSchema(**address.model_dump())
