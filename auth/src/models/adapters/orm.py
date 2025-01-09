import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    MetaData,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry, relationship

from src.models.permissions import Permission
from src.models.roles import RolePermission, Role
from src.models.sessions import Session
from src.models.users import User

mapper_registry = registry()
metadata = MetaData()


class TimestampMixin:
    """Миксин для добавления полей создания и обновления"""

    @staticmethod
    def create_timestamp_columns():
        """Создает столбцы с метками времени для каждой таблицы."""
        return (
            Column("created_at", DateTime, default=datetime.utcnow, nullable=False),
            Column(
                "updated_at",
                DateTime,
                default=datetime.utcnow,
                onupdate=datetime.utcnow,
                nullable=False,
            ),
        )


users_table = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", String(255), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("full_name", String(255), nullable=True),
    Column("role_id", ForeignKey("roles.id", ondelete="SET NULL"), nullable=True),
    *TimestampMixin.create_timestamp_columns(),
    Index("ix_users_email", "email"),
)

roles_table = Table(
    "roles",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(255), nullable=False, unique=True),
)

permissions_table = Table(
    "permissions",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("slug", String(255), nullable=False, unique=True),
    Column("title", String(255), nullable=True),
    Column("description", String(255), nullable=True),
)

role_permission_table = Table(
    "role_permission",
    metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True),
    Column(
        "permission_id",
        UUID(as_uuid=True),
        ForeignKey("permissions.id"),
        primary_key=True,
    ),
    Index("ix_role_permission_role_id", "role_id"),
    Index("ix_role_permission_permission_id", "permission_id"),
)

sessions_table = Table(
    "sessions",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("device", String(255), nullable=True),
    Column("location", String(255), nullable=True),
    Column("jti", UUID(as_uuid=True), nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("is_active", Boolean(), default=True, nullable=False),
    *TimestampMixin.create_timestamp_columns(),
    Index("ix_sessions_user_id", "user_id"),
)


def map_users():
    mapper_registry.map_imperatively(
        class_=User,
        local_table=users_table,
        properties={
            "sessions": relationship(Session, back_populates="user", lazy="selectin"),
            "role": relationship(Role, back_populates="users", lazy="joined"),
        },
    )

    mapper_registry.map_imperatively(
        class_=Session,
        local_table=sessions_table,
        properties={
            "user": relationship(User, back_populates="sessions"),
        },
    )


def map_roles_permissions():
    mapper_registry.map_imperatively(
        class_=Role,
        local_table=roles_table,
        properties={
            "users": relationship(User, back_populates="role"),
            "permissions": relationship(
                Permission,
                secondary=role_permission_table,
                back_populates="role",
                lazy="selectin",
            ),
        },
    )
    mapper_registry.map_imperatively(
        class_=Permission,
        local_table=permissions_table,
        properties={
            "role": relationship(
                Role,
                secondary=role_permission_table,
                back_populates="permissions",
            ),
        },
    )
    mapper_registry.map_imperatively(
        class_=RolePermission, local_table=role_permission_table
    )


def start_mappers():
    map_users()
    map_roles_permissions()
