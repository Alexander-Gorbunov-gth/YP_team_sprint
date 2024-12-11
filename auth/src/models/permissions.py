import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres import Base
from .mixins import TimestampMixin


class Permission(Base, TimestampMixin):
    __tablename__ = 'permissions'

    slug = Column(String(255), primary_key=True, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255))

    def __repr__(self) -> str:
        return f'<Permission {self.slug}>'
