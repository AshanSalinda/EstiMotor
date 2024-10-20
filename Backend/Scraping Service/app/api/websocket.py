import asyncio
from typing import List
from app.utils.logger import info, warn, err
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
active_connections: List[WebSocket] = []
message_queue = asyncio.Queue()
is_enqueue_access_granted = False
send_task: asyncio.Task = None
batch_size = 5   # Number of messages to send at once


def enqueue_for_sending(message: dict):
    """Add a message to the queue for sending."""
    global is_enqueue_access_granted
    if not is_enqueue_access_granted:
        return
    try:
        message_queue.put_nowait(message)
    except asyncio.QueueFull:
        warn("Message queue is full. Skipping message..")
        
        
def set_enqueue_access(access: bool):
    """To control the access when starting and stopping crawling process"""
    global is_enqueue_access_granted
    is_enqueue_access_granted = access
    cleanup_queue()
        
        
def cleanup_queue():
    if not message_queue.empty():
        # cleanup the queue
        try:
            while not message_queue.empty():    
                message_queue.get_nowait()
        except asyncio.QueueEmpty:
            pass



async def cancel_sender_task():
    """Cancel the send_messages coroutine."""
    global send_task
    if send_task:
        send_task.cancel()  # Cancel the task
        cleanup_queue()
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
            err(f"Error sending message to {connection}:", e)



async def check_for_send():
    while True:
        messages = []
        while not message_queue.empty() and len(messages) < batch_size:
            message = await message_queue.get()
            messages.append(message)

        if messages:
            await broadcast(messages)
        
        await asyncio.sleep(0.1)



@router.on_event("shutdown")
async def on_shutdown():
    """Shutdown event to cancel the send_messages coroutine."""
    await cancel_sender_task()



@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)

    global send_task
    if send_task is None:
        send_task = asyncio.create_task(check_for_send())
    
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        if not active_connections:
            await cancel_sender_task()
    



