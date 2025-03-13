import uuid

from sqlalchemy.orm import registry
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, String, Boolean, ForeignKey

from src.domain.entities import User, Permission, Role

mapper_registry = registry()

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", String(255), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("is_active", Boolean(), default=False, nullable=False),
)

mapper_registry.map_imperatively(User, users_table)


permissions_table = Table(
    "permissions",
    mapper_registry.metadata,
    Column("slug", String(255), primary_key=True),
    Column("description", String(255), nullable=True)
)

mapper_registry.map_imperatively(Permission, permissions_table)


role_table = Table(
    "roles",
    mapper_registry.metadata,
    Column("slug", String(255), primary_key=True),
    Column("title", String(255), nullable=False),
    Column("description", String(255), nullable=True),
)

mapper_registry.map_imperatively(Role, role_table)


role_permissions_table = Table(
    "role_permissions",
    mapper_registry.metadata,
    Column("role_slug", String(255), ForeignKey("roles.slug", ondelete="CASCADE"), primary_key=True),
    Column("permission_slug", String(255), ForeignKey("permissions.slug", ondelete="CASCADE"), primary_key=True)
)

mapper_registry.map_imperatively(
    Permission,
    permissions_table,
    properties={
        "roles": relationship(
            "Role",
            secondary=role_permissions_table,
            back_populates="permissions"
        )
    }
)

mapper_registry.map_imperatively(
    Role,
    role_table,
    properties={
        "permissions": relationship(
            "Permission",
            secondary=role_permissions_table,
            back_populates="roles"
        )
    }
)