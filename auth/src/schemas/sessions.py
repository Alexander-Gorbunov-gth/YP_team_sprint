from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class SessionCreate(BaseModel):
    user_id: UUID
    device: str = Field(default="unknown")
    location: str = Field(default="unknown")
    jti: UUID
    expires_at: datetime
