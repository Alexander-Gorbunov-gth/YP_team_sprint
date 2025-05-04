import uuid
import asyncio
import logging

from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from src.core.config import settings
from src.api.v1.schemas import Event
from src.domain.entities import ClientEvent
from src.api.v1.dedpendencies import storage_repoDep, producerDep
from src.infrastructure.storage import AbstractStorageRepository
from src.infrastructure.producer import AbstractProducerBroker

route = APIRouter()


@route.post("/event/{event_type}/")
async def client_event(
    request: Request,
    event: Event,
    event_type: str,
    storage_repo: storage_repoDep,
    producer: producerDep
):
    request_id = str(uuid.uuid4())
    try:    
        client_event = ClientEvent(
            user_agent=request.headers.get("user-agent"),
            user_ip=request.client.host,
            event_type=event_type,
            payload=event.payload,
        )
        await storage_repo.add(key=request_id, value=client_event.model_dump_json())
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    message = {"request_id": request_id, "token": event.token}
    asyncio.create_task(producer.send_message(topic=settings.brocker.auth_topic_name, value=message, key=settings.brocker.auth_topic_key))
    return {"ok": True}


@route.post("/ping")
async def ping():
    return {"pong": True}
