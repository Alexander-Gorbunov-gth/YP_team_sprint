from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.api.v1.depends import Current_User_Dep
from src.services.handlers.push import active_connections

router = APIRouter(prefix="/ws", tags=["Websockets"])


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket, current_user: Current_User_Dep):
    """Websocket для отправки сообщений"""

    await websocket.accept()
    active_connections[current_user["sub"]] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        del active_connections[current_user["sub"]]
