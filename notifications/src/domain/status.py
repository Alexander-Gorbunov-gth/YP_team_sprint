from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class MessageStatus(str, Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    error = "error"
    sent = "sent"


class MessageModel(BaseModel):
    id: UUID
    body: str
    send_at: datetime | None = None
    sent_to: UUID
    sent_address: str
    status: MessageStatus
    subject: str | None = None
    created_at: datetime
    updated_at: datetime
