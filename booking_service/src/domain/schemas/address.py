from uuid import UUID

from pydantic import BaseModel, Field


class AddressBaseSchema(BaseModel):
    country: str
    city: str
    street: str
    house: str
    flat: str | None = Field(default=None)


class AdressCreateSchema(AddressBaseSchema):
    pass


class AdressRepresentSchema(AddressBaseSchema):
    id: UUID


class UpdateAddressSchema(BaseModel):
    country: str | None
    city: str | None
    street: str | None
    house: str | None
    flat: str | None
