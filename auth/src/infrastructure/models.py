import uuid

from sqlalchemy.orm import registry
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, String, Boolean

from src.domain.entities import User

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
