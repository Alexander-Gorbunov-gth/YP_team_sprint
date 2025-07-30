from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.domain.entities.event import Event
from src.domain.entities.reservation import Reservation
from src.infrastructure.models.base import mapper_registry, timestamp_columns

events = Table(
    "events",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("movie_id", UUID(as_uuid=True), nullable=False),
    Column("address_id", UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False),
    Column("owner_id", UUID(as_uuid=True), nullable=False),
    Column("capacity", Integer, nullable=False),
    Column("start_datetime", DateTime, nullable=False),
    *timestamp_columns(),
)


mapper_registry.map_imperatively(
    Event,
    events,
    properties={
        "reservations": relationship(
            Reservation,
            back_populates="event",
            cascade="all, delete-orphan",
            lazy="joined",
        ),
    },
)
