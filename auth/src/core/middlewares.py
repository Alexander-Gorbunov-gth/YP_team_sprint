import logging
import time
from typing import Callable

from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.db.redis import get_redis

logger = logging.getLogger(__name__)


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, limit: int = 100, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next: Callable):
        try:
            redis = await get_redis()
        except Exception:
            logger.warning("Redis is not initialized.")
            return await call_next(request)
        id = request.headers.get("X-Request-Id") or "unknown"
        now = int(time.time())
        window_key = f"rate_limit:{id}:{now // self.window}"
        logger.info(f"Rate limit key: {window_key}")

        try:
            current = await redis.incr(window_key)
            logger.info(f"Current rate limit: {current}")
            if current == 1:
                await redis.expire(window_key, self.window)

            if current > self.limit:
                logger.warning(f"Rate limit exceeded for {id}")
                return ORJSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Too Many Requests"},
                )

        except Exception as e:
            logger.error(f"Rate limiter error: {e}")
            pass

        return await call_next(request)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Проверяет наличие заголовка X-Request-Id для трасировки запросов"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-Id")
        if request_id is None:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "X-Request-Id is required"},
            )

        response = await call_next(request)
        return response
