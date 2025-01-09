from dataclasses import dataclass
from uuid import UUID

from src.models.interfaces import IModel
from src.models.mixins import IdMixinModel, TimestampMixinModel


@dataclass
class User(IdMixinModel, TimestampMixinModel, IModel):
    email: str
    password: str
    full_name: str | None
    role_id: UUID | None
