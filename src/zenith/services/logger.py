"""Structured JSON logging engine."""

import json
import logging
import sys


class StructuredLogger:
    def __init__(self, name: str = "zenith"):
        self.name = name
        self.correlation_id = None

    def log(self, level: str, message: str, **kwargs) -> None:
        entry = {"level": level, "logger": self.name, "msg": message, **kwargs}
        sys.stdout.write(json.dumps(entry) + "\n")
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
    def info(self, msg: str, **kwargs) -> None:
        payload = {'msg': msg, 'correlation_id': self.correlation_id, **kwargs}
        self._sink.write(json.dumps(payload) + '\n')
