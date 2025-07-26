from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from src.domain.entities.subscription import Subscription

mapper_registry = registry()


def timestamp_columns():
    return [
        Column("created_at", DateTime, nullable=False, default=datetime.now(timezone.utc).replace(tzinfo=None)),
        Column(
            "updated_at",
            DateTime,
            nullable=False,
            default=datetime.now(timezone.utc).replace(tzinfo=None),
            onupdate=datetime.now(timezone.utc).replace(tzinfo=None),
        ),
    ]


subscriptions = Table(
    "subscriptions",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("host_id", UUID(as_uuid=True), nullable=False),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    *timestamp_columns(),
)


mapper_registry.map_imperatively(Subscription, subscriptions)
