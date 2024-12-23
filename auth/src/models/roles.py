from dataclasses import dataclass
from uuid import UUID

from src.models.interfaces import IModel
from src.models.mixins import IdMixinModel


@dataclass
class Role(IdMixinModel, IModel):
    title: str


@dataclass
class RolePermission(IModel):
    role_id: UUID
    permission_id: UUID
