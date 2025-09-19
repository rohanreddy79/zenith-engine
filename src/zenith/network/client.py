"""Async HTTP & RPC client with connection pooling."""

import httpx
from typing import Any, Optional


class AsyncHttpClient:
    def __init__(self, timeout: float = 10.0, max_connections: int = 100):
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout, limits=httpx.Limits(max_connections=max_connections))

    async def get(self, url: str) -> httpx.Response:
        return await self.client.get(url)

    async def post(self, url: str, json: Any) -> httpx.Response:
        return await self.client.post(url, json=json)

    async def close(self) -> None:
        await self.client.aclose()
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
    async def acquire_healthy_connection(self) -> 'Connection':
        conn = await self._pool.acquire()
        if not conn.is_alive():
            conn = await self._reconnect(conn)
        return conn
