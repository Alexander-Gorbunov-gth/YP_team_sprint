import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
# from src.api.v1.schemas.events import

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profile", tags=["Profile"])



