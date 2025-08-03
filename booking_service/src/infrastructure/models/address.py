from uuid import uuid4

from sqlalchemy import Column, Float, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.domain.entities.address import Address
from src.infrastructure.models.event import Event
from src.infrastructure.models.base import mapper_registry, timestamp_columns

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

def mapped_addresses_table():
    mapper_registry.map_imperatively(Address, addresses, properties={
        "events": relationship(
            Event,
            back_populates="address",
            lazy="joined",
        ),
    })
