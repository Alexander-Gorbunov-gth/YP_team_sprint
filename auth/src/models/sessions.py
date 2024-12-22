from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.models.interfaces import IModel
from src.models.mixins import IdMixinModel, TimestampMixinModel


@dataclass
class Session(IdMixinModel, TimestampMixinModel, IModel):
    user_id: UUID
    device: str
    location: str
    jti: UUID
    expires_at: datetime
    is_active: bool = True
