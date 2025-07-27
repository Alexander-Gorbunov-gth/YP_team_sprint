import logging

from fastapi import APIRouter

from src.api.v1.schemas.address import AddressCreateSchema, AddressResponseSchema, UpdateAddressSchema
from tests.unit.routers_fixture import address_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/address", tags=["Address"])


@router.post("/", summary="Создать адрес", response_model=AddressResponseSchema)
async def create_address(data: AddressCreateSchema):
    return address_data


@router.get(
    "/{id}",
    summary="Получить данные об адресе",
    response_model=AddressResponseSchema,
)
async def get_address():
    return address_data


@router.get(
    "/my/",
    summary="Получить список моих адресов",
    response_model=list[AddressResponseSchema | None],
)
async def get_my_address():
    return [address_data]


@router.delete("/{id}", summary="Удалить адрес")
async def delete_address() -> bool:
    return True


@router.patch("/{id}", summary="Изменить адрес", response_model=AddressResponseSchema)
async def update_address(data: UpdateAddressSchema):
    return address_data
