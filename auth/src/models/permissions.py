from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.postgres import Base
from .mixins import TimestampMixin


class Permission(Base, TimestampMixin):
    __tablename__ = 'permissions'

    slug = Column(String(255), primary_key=True, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    user_permissions = relationship(
        'UserPermissionsAssociation',
        back_populates='permission'
    )
    users = relationship('User', secondary='user_permission_association', back_populates='permissions')

    def __repr__(self) -> str:
        return f'<Permission {self.slug}>'


class UserPermissionsAssociation(Base):
    __tablename__ = 'user_permission_association'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    permission_slug = Column(String(255), ForeignKey('permissions.slug'), primary_key=True)

    user = relationship("User", back_populates="user_permissions")
    permission = relationship("Permission", back_populates="user_permissions")


class PermissionCreate(BaseModel):
    slug: str
    title: str
    description: Optional[str] = None


class PermissionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class PermissionPublic(PermissionCreate):
    pass
