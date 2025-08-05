from uuid import uuid4

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.domain.entities.feedback import Feedback, ReviewType
from src.infrastructure.models.base import mapper_registry, timestamp_columns

feedbacks = Table(
    "feedbacks",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    Column("event_id", UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False),
    Column(
        "review", Enum(ReviewType, name="review_type"), nullable=False
    ),
    *timestamp_columns(),
)


def mapped_feedbacks_table():
    mapper_registry.map_imperatively(
        Feedback,
        feedbacks,
        properties={
            "event": relationship(
                "Event",
                back_populates="feedbacks",
                lazy="selectin",
            ),
        },
    )
