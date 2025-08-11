from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.v1.schemas.errors import ErrorResponse, ErrorPayload
from src.services import exceptions as exc
from src.domain import exceptions as domain_exc


EXC_MAP: dict[type[Exception], tuple[int, str]] = {
    exc.EventTimeConflictError: (409, "EVENT_TIME_CONFLICT"),
    exc.EventNotFoundError: (404, "EVENT_NOT_FOUND"),
    exc.EventStartDatetimeError: (400, "EVENT_START_DATETIME_INVALID"),
    exc.EventNotOwnerError: (403, "EVENT_NOT_OWNER"),
    exc.ReservationNotFoundError: (404, "RESERVATION_NOT_FOUND"),
    exc.SessionHasExpired: (401, "SESSION_EXPIRED"),
    exc.AddressNotFoundError: (404, "ADDRESS_NOT_FOUND"),
    exc.ForbiddenError: (403, "FORBIDDEN"),
    exc.SubscriptionAlreadyExistsError: (409, "SUBSCRIPTION_ALREADY_EXISTS"),
    exc.SubscriptionNotFoundError: (404, "SUBSCRIPTION_NOT_FOUND"),
    exc.FeedbackNotFoundError: (404, "FEEDBACK_NOT_FOUND"),
    exc.EventFeedbackNotStartedError: (400, "EVENT_FEEDBACK_NOT_STARTED"),
    exc.EventFeedbackOwnerError: (400, "EVENT_FEEDBACK_OWNER"),
    exc.UserFeedbackSelfError: (400, "USER_FEEDBACK_SELF"),
    exc.UserFeedbackUserNotFoundError: (400, "USER_NOT_IN_EVENT"),
    domain_exc.AddressNotFoundError: (400, "AddressNotFound"),
    domain_exc.DuplicateReservationError: (400, "DuplicateReservation"),
    domain_exc.EventUpdateLockedError: (400, "EventUpdateLocked"),
    domain_exc.NotAvailable: (400, "NotAvailable"),
    domain_exc.NotEnoughSeatsError: (400, "NotEnoughSeats"),
}


def _make_handler(status_code: int, code: str):
    async def handler(_: Request, err: Exception):
        payload = ErrorPayload(code=code, message=str(err), details=None)
        return JSONResponse(
            status_code=status_code, content=ErrorResponse(error=payload).model_dump()
        )

    return handler


def init_exception_handlers(app: FastAPI) -> None:
    for exc_type, (status_code, code) in EXC_MAP.items():
        app.add_exception_handler(exc_type, _make_handler(status_code, code))
