"""Environment and configuration loader."""

import os
from typing import Any, Dict


class ConfigLoader:
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        return os.environ.get(f"ZENITH_{key}", default)
