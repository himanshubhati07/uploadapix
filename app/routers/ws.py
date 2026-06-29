# WebSocket routes.
from fastapi import APIRouter, WebSocket

router = APIRouter(tags=["ws"])


@router.websocket("/ws/ping")
async def websocket_ping(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("pong")
    await websocket.close()
