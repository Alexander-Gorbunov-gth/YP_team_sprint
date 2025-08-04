from uuid import uuid4

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.domain.entities.reservation import Reservation, ReservationStatus
from src.infrastructure.models.base import mapper_registry, timestamp_columns

reservations = Table(
    "reservations",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    Column("event_id", UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False),
    Column("seats", Integer, nullable=False),
    Column(
        "status", Enum(ReservationStatus, name="reservation_status"), nullable=False, default=ReservationStatus.PENDING
    ),
    *timestamp_columns(),
)


def mapped_reservations_table():
    mapper_registry.map_imperatively(
        Reservation,
        reservations,
        properties={
            "event": relationship(
                "Event",
                back_populates="reservations",
                lazy="selectin",
            ),
        },
    )
