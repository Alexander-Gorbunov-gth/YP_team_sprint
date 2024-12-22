from dataclasses import dataclass, field

from src.models.interfaces import IModel
from src.models.mixins import IdMixinModel, TimestampMixinModel


@dataclass
class Permission(IdMixinModel, TimestampMixinModel, IModel):
    slug: str
    title: str = field(init=False)
    description: str = field(init=False)
