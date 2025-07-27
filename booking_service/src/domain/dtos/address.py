from uuid import UUID

from pydantic import BaseModel, Field


class AdressCreateDTO(BaseModel):
    country: str
    city: str
    street: str
    house: str
    flat: str | None = Field(default=None)


class AddressUpdateDTO(BaseModel):
    id: UUID
    country: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    flat: str | None = None
