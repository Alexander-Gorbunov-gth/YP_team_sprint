from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TimestampMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | None = Field(default=None, description="ID документа")
    created_at: datetime = Field(default_factory=datetime.now, description="Дата создания документа")
    updated_at: datetime = Field(default_factory=datetime.now, description="Дата обновления документа")

    def touch(self):
        self.updated_at = datetime.now()
