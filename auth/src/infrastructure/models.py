import uuid
from datetime import datetime

from sqlalchemy.orm import registry
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, String, Boolean, ForeignKey, Index, DateTime

from src.domain.entities import User, Session

mapper_registry = registry()


def timestamp_columns():
    return [
        Column("created_at", DateTime, nullable=False, default=datetime.now()),
        Column("updated_at", DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    ]


users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", String(255), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("is_active", Boolean(), default=False, nullable=False),
    *timestamp_columns()
)

sessions_table = Table(
    "sessions",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("user_agent", String(255), nullable=False),
    Column("jti", UUID(as_uuid=True), nullable=False, unique=True),
    Column("refresh_token", String(1055), nullable=False, unique=True),
    Column("user_ip", String(255), nullable=True),
    Column("is_active", Boolean(), nullable=False, default=True),
    *timestamp_columns(),
    Index("idx_session_user_id", "user_id"),   
)


mapper_registry.map_imperatively(User, users_table)
mapper_registry.map_imperatively(Session, sessions_table)
