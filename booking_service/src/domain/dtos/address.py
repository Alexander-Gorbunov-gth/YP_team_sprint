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
    country: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    flat: str | None = None
