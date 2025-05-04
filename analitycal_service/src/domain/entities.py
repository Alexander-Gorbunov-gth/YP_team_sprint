from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ClickPayload(BaseModel):
    item_id: str
    item_type: str


class PageViewPayload(BaseModel):
    page_type: str
    duration_seconds: int


class QualityChangePayload(BaseModel):
    video_id: str
    from_quality: str
    to_quality: str
    current_time_seconds: int


class VideoFinishedPayload(BaseModel):
    video_id: str
    total_duration_seconds: int


class SearchFilterPayload(BaseModel):
    filters: list[str]


class VideoProgressPayload(BaseModel):
    video_id: str
    watched_seconds: int


class ClientEvent(BaseModel):
    user_id: UUID | str | None = Field(default=None)
    user_ip: str
    user_agent: str
    event_type: Literal[
        "click", "page_view", "quality_change", "video_finished", "search_filter_used", "video_progress"
    ]
    timestamp: datetime = Field(default_factory=datetime.now)
    payload: (
        ClickPayload
        | PageViewPayload
        | QualityChangePayload
        | VideoFinishedPayload
        | SearchFilterPayload
        | VideoProgressPayload
    )
