from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class IdMixinModel:
    id: UUID = field(init=False)


@dataclass
class TimestampMixinModel:
    created_at: datetime = field(init=False)
    updated_at: datetime = field(init=False)
