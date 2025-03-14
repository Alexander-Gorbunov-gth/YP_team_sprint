import uuid
from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Index, String,
                        Table)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry, relationship

from src.domain.entities import Permission, Role, Session, User

mapper_registry = registry()


def timestamp_columns():
    return [
        Column("created_at", DateTime, nullable=False, default=datetime.now()),
        Column("updated_at", DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now()),
    ]


users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", String(255), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("is_active", Boolean(), default=False, nullable=False),
    *timestamp_columns(),
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

permissions_table = Table(
    "permissions",
    mapper_registry.metadata,
    Column("slug", String(255), primary_key=True),
    Column("description", String(255), nullable=True),
)

# mapper_registry.map_imperatively(Permission, permissions_table)


role_table = Table(
    "roles",
    mapper_registry.metadata,
    Column("slug", String(255), primary_key=True),
    Column("title", String(255), nullable=False),
    Column("description", String(255), nullable=True),
)

# mapper_registry.map_imperatively(Role, role_table)


role_permissions_table = Table(
    "role_permissions",
    mapper_registry.metadata,
    Column("role_slug", String(255), ForeignKey("roles.slug", ondelete="CASCADE"), primary_key=True),
    Column("permission_slug", String(255), ForeignKey("permissions.slug", ondelete="CASCADE"), primary_key=True),
)

mapper_registry.map_imperatively(
    Permission,
    permissions_table,
    properties={"roles": relationship("Role", secondary=role_permissions_table, back_populates="permissions")},
)

mapper_registry.map_imperatively(
    Role,
    role_table,
    properties={"permissions": relationship("Permission", secondary=role_permissions_table, back_populates="roles")},
)
