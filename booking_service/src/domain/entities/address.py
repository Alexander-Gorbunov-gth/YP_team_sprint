from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.domain.entities.mixins import DateTimeMixin


class Address(DateTimeMixin, BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    latitude: float
    longitude: float
    country: str
    city: str
    street: str
    house: str
    flat: str | None = Field(default=None)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)

    @classmethod
    def create(
        cls,
        user_id: UUID,
        latitude: float,
        longitude: float,
        country: str,
        city: str,
        street: str,
        house: str,
        flat: str | None = None,
    ) -> "Address":
        return cls(
            user_id=user_id,
            latitude=latitude,
            longitude=longitude,
            country=country,
            city=city,
            street=street,
            house=house,
            flat=flat,
        )

    @property
    def full_address(self) -> str:
        if self.flat is not None:
            return f"{self.country}, {self.city}, {self.street}, {self.house}, {self.flat}"
        return f"{self.country}, {self.city}, {self.street}, {self.house}"

    @property
    def public_address(self) -> str:
        return f"{self.country}, {self.city}, {self.street}"
