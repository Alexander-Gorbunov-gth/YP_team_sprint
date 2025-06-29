from datetime import datetime
from typing import Dict, List
from uuid import UUID

from pydantic import BaseModel
from src.domain.channels import ChannelTypes


class Template(BaseModel):
    id: UUID
    channel: ChannelTypes
    event_type: str
    subject: str | None
    body: str
