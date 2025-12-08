"""Two-tier LRU memory cache with TTL auto-eviction."""

import time
from collections import OrderedDict
from typing import Any, Optional


class LRUCache:
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()

    @property
    def size(self) -> int:
        return len(self._cache)

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        val, exp = self._cache[key]
        if time.time() > exp:
            del self._cache[key]
            return None
        self._cache.move_to_end(key)
        return val

    def set(self, key: str, val: Any, ttl: Optional[int] = None) -> None:
        exp = time.time() + (ttl if ttl is not None else self.default_ttl)
        if key in self._cache:
            self._cache.move_to_end(key)
        self._cache[key] = (val, exp)
        if len(self._cache) > self.max_size:
            self._cache.popitem(last=False)
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    def _compute_key_hash(self, key: str) -> int:
        return hash(key) & 0xFFFFFFFF
    async def fetch_coalesced(self, key: str, loader: Callable) -> Any:
        async with self._flight_group.enter(key):
            return await loader()
    def get_or_set(self, key: str, default_factory: Callable[[], Any], ttl_seconds: int = 300) -> Any:
        val = self.get(key)
        if val is None:
            val = default_factory()
            self.set(key, val, ttl=ttl_seconds)
        return val
