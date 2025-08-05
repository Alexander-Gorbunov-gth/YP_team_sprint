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
from src.infrastructure.models.address import Address
from src.infrastructure.models.base import mapper_registry, timestamp_columns
from src.infrastructure.models.feedback import Feedback

events = Table(
    "events",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("movie_id", UUID(as_uuid=True), nullable=False),
    Column("address_id", UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False),
    Column("owner_id", UUID(as_uuid=True), nullable=False),
    Column("capacity", Integer, nullable=False),
    Column("start_datetime", DateTime(timezone=True), nullable=False),
    *timestamp_columns(),
)


def mapped_events_table():
    mapper_registry.map_imperatively(
        Event,
        events,
        properties={
            "reservations": relationship(
                Reservation,
                back_populates="event",
                cascade="all, delete-orphan",
                lazy="selectin",
            ),
            "address": relationship(
                Address,
                back_populates="events",
                lazy="selectin",
            ),
            "feedbacks": relationship(
                Feedback,
                back_populates="event",
                lazy="selectin",
            ),
        },
    )
