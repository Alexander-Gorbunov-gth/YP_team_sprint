from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    String,
    Table,
)
from sqlalchemy.orm import registry

from src.domain.entities import ShortUrl

mapper_registry = registry()


def timestamp_columns():
    return [
        Column(
            "created_at", DateTime,
            nullable=False,
            default=datetime.now(timezone.utc).replace(tzinfo=None)
        ),
        Column(
            "updated_at", DateTime,
            nullable=False,
            default=datetime.now(timezone.utc).replace(tzinfo=None),
            onupdate=datetime.now(timezone.utc).replace(tzinfo=None)
        ),
    ]


short_urls = Table(
    "short_urls",
    mapper_registry.metadata,
    Column("short_url", String(8), primary_key=True),
    Column("original_url", String(2048), nullable=False),
    Column("expires_at", DateTime, nullable=False),
    *timestamp_columns(),
)


mapper_registry.map_imperatively(ShortUrl, short_urls)
