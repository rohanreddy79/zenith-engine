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
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def compact_wal(self) -> int:
        return self._wal_writer.rotate_and_compact(self._snapshot.current_seq())
    def scan_prefix(self, prefix: str, limit: int = 100) -> List[Tuple[str, bytes]]:
        return self._btree.range_query(start=prefix, end=prefix + '\xFF', limit=limit)
