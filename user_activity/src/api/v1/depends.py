from typing import Annotated

from fastapi import Depends
from src.services.bookmark import AbstractBookmarkService, get_bookmark_service

bookmark_serviceDep = Annotated[AbstractBookmarkService, Depends(get_bookmark_service)]
