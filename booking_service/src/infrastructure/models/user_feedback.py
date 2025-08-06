from uuid import uuid4

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.domain.entities.feedback import ReviewType, UserFeedback
from src.infrastructure.models.base import mapper_registry, timestamp_columns

user_feedbacks = Table(
    "user_feedbacks",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("owner_id", UUID(as_uuid=True), nullable=False),
    Column("user_id", UUID(as_uuid=True), nullable=False),
    Column(
        "review", Enum(ReviewType, name="review_type"), nullable=False
    ),
    *timestamp_columns(),
)


def mapped_user_feedbacks_table():
    mapper_registry.map_imperatively(
        UserFeedback,
        user_feedbacks,
    )
