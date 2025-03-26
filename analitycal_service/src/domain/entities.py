from uuid import UUID
from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field


class ClientEvent(BaseModel):
    user_id: UUID | str
    user_ip: str
    user_agent: str
    event_type: Literal["click"]
    timestamp: datetime = Field(default_factory=datetime.now())
    payload: dict[str, str]
