import asyncio
from typing import AsyncGenerator

from lws.models import Message

class Broker:
    def __init__(self) -> None:
        self.connections = set()

    async def publish(self, message: str, store=True) -> None:
        for connection in self.connections:
            Message(message=message).save()
            await connection.put(message)

    async def subscribe(self) -> AsyncGenerator[str, None]:
        connection = asyncio.Queue()
        self.connections.add(connection)
        try:
            while True:
                yield await connection.get()
        finally:
            self.connections.remove(connection)
