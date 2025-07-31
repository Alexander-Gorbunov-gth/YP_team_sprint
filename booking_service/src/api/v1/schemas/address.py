from uuid import UUID

from pydantic import BaseModel, Field


class AddressBaseSchema(BaseModel):
    country: str
    city: str
    latitude: float
    longitude: float
    street: str
    house: str
    flat: str | None = Field(default=None)


class AddressCreateSchema(AddressBaseSchema):
    pass


class AddressResponseSchema(AddressBaseSchema):
    id: UUID


class UpdateAddressSchema(BaseModel):
    country: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    flat: str | None = None
