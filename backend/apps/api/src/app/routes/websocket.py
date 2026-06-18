from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.app.websocket.connection_manager import manager

router = APIRouter(prefix="/ws",tags=["Websocket"])

@router.websocket("/channels/{business_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    business_id: str
):
    await manager.connect(
        business_id,
        websocket
    )

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(
            business_id,
            websocket
        )