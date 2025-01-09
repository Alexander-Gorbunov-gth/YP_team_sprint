from dataclasses import dataclass

from src.models.interfaces import IModel
from src.models.mixins import IdMixinModel


@dataclass
class Permission(IdMixinModel, IModel):
    slug: str
    title: str
    description: str
