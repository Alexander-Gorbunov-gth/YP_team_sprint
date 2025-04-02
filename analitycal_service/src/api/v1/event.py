from pydantic import ValidationError
from fastapi import APIRouter, Depends, Request, HTTPException

from src.api.v1.schemas import Event
from src.domain.entities import ClientEvent
from src.services.event import AbstractEventService, get_event_service


route = APIRouter()


@route.post("/event/{event_type}/")
async def client_event(
    request: Request, event: Event, event_type: str, event_service: AbstractEventService = Depends(get_event_service)
):
    try:
        client_event = ClientEvent(
            user_id=event.user_id,
            user_agent=request.headers.get("user-agent"),
            user_ip=request.client.host,
            event_type=event_type,
            payload=event.payload,
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    await event_service.handle_event(event=client_event, event_type=event_type)
    return {"ok": True}
