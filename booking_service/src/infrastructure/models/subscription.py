from uuid import uuid4

from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID

from src.domain.entities.address import Address
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


def mapped_subscription_table():
    mapper_registry.map_imperatively(Subscription, subscriptions)


def mapped_address_table():
    mapper_registry.map_imperatively(Address, addresses)
