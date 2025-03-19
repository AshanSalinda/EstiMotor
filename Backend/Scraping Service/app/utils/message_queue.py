import asyncio
from app.utils.logger import info, warn, err

class MessageQueue(object):
    """A static message queue class for WebSocket communication."""
    
    _queue = asyncio.Queue()
    _is_enqueue_access_granted = False
    
    def __new__(cls, *args, **kwargs):
        raise TypeError("MessageQueue is a static class and cannot be instantiated. Use class methods instead.")

 
    @classmethod
    def enqueue(cls, message: dict):
        """Add a message to the queue for sending."""
        if not cls._is_enqueue_access_granted:
            return
        try:
            cls._queue.put_nowait(message)
        except asyncio.QueueFull:
            err("Message queue is full.")
      
      
    @classmethod      
    def set_enqueue_access(cls, access: bool):
        """To control the access when starting and stopping crawling process"""
        cls._is_enqueue_access_granted = access
        cls.clear()
        
        
    @classmethod
    def clear(cls):
        cls._queue._queue.clear()

    
    @classmethod     
    async def get_as_payload(cls, batch_size: int):
        payload = {}
        for _ in range(batch_size):
            data = await cls._queue.get()
            
            cls.format_payload(payload, data)
            
            if cls._queue.empty():
                break
        return payload


    @classmethod
    def format_payload(cls, payload, data):
        if 'progress' in data:
            payload['progress'] = data['progress']
            
        if 'stats' in data:
            payload['stats'] = data['stats']
            
        if 'control' in data:
            payload['control'] = data['control']
            
        if 'log' in data:
            if 'logs' not in payload:
                payload['logs'] = []
            payload['logs'].append(data['log'])