"""Unit tests for LRUCache and KVStore."""

import time
from zenith.storage.cache import LRUCache


def test_lru_eviction():
    cache = LRUCache(max_size=2)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.set("c", 3)
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3
