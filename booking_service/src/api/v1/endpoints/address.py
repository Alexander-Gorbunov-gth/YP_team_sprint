import logging

from fastapi import APIRouter

from src.domain.schemas import address as schema
from tests.unit.routers_fixture import address_data

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/address", tags=["Address"])


@router.post("/", summary="Создать адрес", response_model=schema.AdressRepresentSchema)
async def create_address(data: schema.AdressCreateSchema):
    return address_data


@router.get(
    "/{id}",
    summary="Получить данные об адресе",
    response_model=schema.AdressRepresentSchema,
)
async def get_address():
    return address_data


@router.get(
    "/my/",
    summary="Получить список моих адресов",
    response_model=list[schema.AdressRepresentSchema | None],
)
async def get_my_address():
    return [address_data]


@router.delete("/{id}", summary="Удалить адрес")
async def delete_address() -> bool:
    return True


@router.patch(
    "/{id}", summary="Изменить адрес", response_model=schema.AdressRepresentSchema
)
async def update_address(data: schema.UpdateAddressSchema):
    return address_data
