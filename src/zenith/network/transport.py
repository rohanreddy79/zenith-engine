"""Socket transport and stream buffers."""

import asyncio


class SocketTransport:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer

    async def send_frame(self, data: bytes) -> None:
        self.writer.write(data)
        await self.writer.drain()
