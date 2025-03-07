from dataclasses import dataclass, field

from src.models.interfaces import IModel
from src.models.mixins import IdMixinModel


@dataclass
class Permission(IdMixinModel, IModel):
    slug: str
    title: str = field(init=False)
    description: str = field(init=False)
