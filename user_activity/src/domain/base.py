from datetime import datetime

from pydantic import BaseModel, Field


class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())

    def touch(self):
        self.updated_at = datetime.now()
