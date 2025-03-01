"""Key-value store with Write-Ahead Logging (WAL)."""

from typing import Dict, Optional


class KVStore:
    def __init__(self):
        self._data: Dict[str, bytes] = {}

    def get(self, key: str) -> Optional[bytes]:
        return self._data.get(key)

    def put(self, key: str, value: bytes) -> None:
        self._data[key] = value

    def delete(self, key: str) -> bool:
        return self._data.pop(key, None) is not None
