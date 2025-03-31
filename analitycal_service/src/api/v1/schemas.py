import uuid
from typing import Any

from pydantic import BaseModel


class Event(BaseModel):
    user_id: uuid.UUID | str
    payload: dict[str, Any]
