from datetime import datetime, timezone
from uuid import uuid4
import enum

from sqlalchemy import (
    Column,
    DateTime,
    String,
    Table,
    Enum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from src.domain.status import MessageStatus, MessageModel

mapper_registry = registry()


def timestamp_columns():
    return [
        Column(
            "created_at", DateTime,
            nullable=False,
            default=datetime.now(timezone.utc).replace(tzinfo=None)
        ),
        Column(
            "updated_at", DateTime,
            nullable=False,
            default=datetime.now(timezone.utc).replace(tzinfo=None),
            onupdate=datetime.now(timezone.utc).replace(tzinfo=None)
        ),
    ]


messages = Table(
    "messages",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("body", String(), nullable=False),
    Column("send_at", DateTime),
    Column("sent_to", UUID(as_uuid=True), nullable=False),
    Column("sent_address", String(), nullable=False),
    Column("status", Enum(MessageStatus, name="message_status_enum"), nullable=False),
    Column("subject", String()),
    *timestamp_columns(),
)


mapper_registry.map_imperatively(MessageModel, messages)
