from sqlmodel import SQLModel, Field

from .mixins import DateTimeMixin


class BaseSession(DateTimeMixin):
    ip: str = Field()
    refresh_token: str
    # user = 