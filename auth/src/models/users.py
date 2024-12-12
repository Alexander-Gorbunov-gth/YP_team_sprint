import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.core.auth import verify_password, get_password_hash

from src.db.postgres import Base
from .mixins import TimestampMixin
from .sessions import Session, UserSessionAssociation
from .permissions import Permission, UserPermissionsAssociation


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50),  nullable=True)
    is_superuser = Column(Boolean, default=False)

    user_sessions = relationship(
        UserSessionAssociation,
        back_populates='user'
    )
    sessions = relationship(
        Session,
        secondary='user_session_association',
        back_populates='users'
    )
    user_permissions = relationship(
        UserPermissionsAssociation,
        back_populates='user'
    )
    permissions = relationship(
        Permission,
        secondary='user_permission_association',
        back_populates='users'
    )



    def __init__(
            self,
            login: str,
            password: str,
            first_name: str = "Не указано",
            last_name: str = "Не указано",
            is_superuser: bool = False
    ) -> None:
        self.login = login
        self.password = get_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.is_superuser = is_superuser
    
    def check_password(self, password: str) -> bool:
        return verify_password(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.login}>'
