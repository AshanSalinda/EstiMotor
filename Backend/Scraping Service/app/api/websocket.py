import asyncio
from typing import List
from app.utils.logger import err
from app.utils.message_queue import MessageQueue
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
active_connections: List[WebSocket] = []
send_task: asyncio.Task


async def cancel_sender_task():
    """Cancel the send_messages coroutine."""
    global send_task
    if send_task:
        send_task.cancel()  # Cancel the task
        MessageQueue.clear()
        try:
            await send_task  # Wait for the task to be cancelled
            send_task = None
        except asyncio.CancelledError:
            send_task = None


async def broadcast(message: List[dict]):
    """Send a JSON message to all active WebSocket connections."""
    for connection in active_connections.copy():
        try:
            await connection.send_json(message)
        except WebSocketDisconnect:
            active_connections.remove(connection)
            if not active_connections:
                await cancel_sender_task()
        except RuntimeError as e:
            err(f"Error sending message to {connection}:")
            print(e)

        
async def check_for_send():
    while True:
        payload = await MessageQueue.get_as_payload(5)
        if payload:
            await broadcast(payload)
        await asyncio.sleep(0.1)
        

@router.on_event("shutdown")
async def on_shutdown():
    """Shutdown event to cancel the send_messages coroutine."""
    await cancel_sender_task()


@router.websocket("/")
async def websocket_endpoint(connection: WebSocket):
    await connection.accept()
    active_connections.append(connection)

    global send_task
    if send_task is None:
        send_task = asyncio.create_task(check_for_send())
    
    try:
        while True:
            await connection.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(connection)
        if not active_connections:
            await cancel_sender_task()
