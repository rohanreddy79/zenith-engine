"""Socket transport and stream buffers."""

import asyncio


class SocketTransport:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer

    async def send_frame(self, data: bytes) -> None:
        self.writer.write(data)
        await self.writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    async def write_drained(self, data: bytes) -> None:
        self._writer.write(data)
        if self._writer.transport.get_write_buffer_size() > 65536:
            await self._writer.drain()
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
    def configure_tls_resumption(self, session_cache: 'TlsSessionCache') -> None:
        self._ssl_ctx.set_session_cache_mode(ssl.SESS_CACHE_CLIENT)
