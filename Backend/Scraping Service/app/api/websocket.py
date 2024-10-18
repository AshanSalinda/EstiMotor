from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..utils.logger import info, warn, err
from typing import List

router = APIRouter()
active_connections: List[WebSocket] = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        

async def broadcast(message: dict):
    """Send a JSON message to all active WebSocket connections."""
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except WebSocketDisconnect:
            active_connections.remove(connection)
        except RuntimeError as e:
            err(f"Error sending message to {connection}: {str(e)}")

