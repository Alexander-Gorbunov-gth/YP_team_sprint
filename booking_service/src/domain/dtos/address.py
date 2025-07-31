from uuid import UUID

from pydantic import BaseModel, Field


class AddressCreateDTO(BaseModel):
    user_id: UUID
    latitude: float
    longitude: float
    country: str
    city: str
    street: str
    house: str
    flat: str | None = Field(default=None)


class AddressUpdateDTO(BaseModel):
    latitude: float | None = None
    longitude: float | None = None
    country: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    flat: str | None = None
