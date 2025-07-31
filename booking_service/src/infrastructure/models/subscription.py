from sqlalchemy import (

    Column,
    Integer,
    Table,
)

from sqlalchemy.dialects.postgresql import UUID

from src.domain.entities.subscription import Subscription
from src.infrastructure.models.base import mapper_registry, timestamp_columns

subscriptions = Table(
    "subscriptions",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("host_id", UUID(as_uuid=True), nullable=False),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    *timestamp_columns(),
)

def mapped_subscription_table():
    mapper_registry.map_imperatively(Subscription, subscriptions)
