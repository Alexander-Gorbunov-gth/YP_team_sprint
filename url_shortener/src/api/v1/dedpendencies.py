from typing import Annotated

from fastapi import Depends

from src.services.short_url import ShortUrlService, get_short_url_service

short_urlDep = Annotated[ShortUrlService, Depends(get_short_url_service)]
