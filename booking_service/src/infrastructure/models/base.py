from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
)
from sqlalchemy.orm import registry

mapper_registry = registry()


def timestamp_columns():
    return [
        Column("created_at", DateTime, nullable=False, default=datetime.now(timezone.utc).replace(tzinfo=None)),
        Column(
            "updated_at",
            DateTime,
            nullable=False,
            default=datetime.now(timezone.utc).replace(tzinfo=None),
            onupdate=datetime.now(timezone.utc).replace(tzinfo=None),
        ),
    ]
