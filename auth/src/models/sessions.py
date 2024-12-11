import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from src.db.postgres import Base
from .mixins import TimestampMixin


class Session(Base, TimestampMixin):
    __tablename__ = 'sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    ip = Column(String(255), nullable=False)
    refresh_token = Column(String(500))

    user_sessions = relationship('UserSessionAssociation', back_populates='session')
    users = relationship('User', secondary='user_session_association', back_populates='sessions')

    def __repr__(self) -> str:
        return f'<Session {self.ip}>'


class UserSessionAssociation(Base):
    __tablename__ = 'user_session_association'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.id'), primary_key=True)

    user = relationship("User", back_populates="user_sessions")
    session = relationship("Session", back_populates="user_sessions")
