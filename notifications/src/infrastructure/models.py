import enum
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, registry
from src.domain.status import MessageModel, MessageStatus

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


class TemplateType(enum.Enum):
    EMAIL = "email"
    PUSH = "push"


class Base(DeclarativeBase):
    pass


class TemplateModel(Base):
    __tablename__ = "templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    template = Column(Text, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    channel = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=True)
    *timestamp_columns(),

    def __repr__(self) -> str:
        return f"TemplateModel(id={self.id}, name={self.name}, channel={self.channel})"

    def __str__(self) -> str:
        return f"{self.name} - {self.channel}"
