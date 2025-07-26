from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from src.domain.entities.address import Address
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

addresses = Table(
    "addresses",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    Column("latitude", Float, nullable=False),
    Column("longitude", Float, nullable=False),
    Column("country", String, nullable=False),
    Column("city", String, nullable=False),
    Column("street", String, nullable=False),
    Column("house", String, nullable=False),
    Column("flat", String, nullable=True),
    *timestamp_columns(),
)


mapper_registry.map_imperatively(Subscription, subscriptions)
mapper_registry.map_imperatively(Address, addresses)
