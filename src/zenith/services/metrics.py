"""Prometheus telemetry and latency buckets."""

from typing import Dict


class MetricsRegistry:
    def __init__(self):
        self._counters: Dict[str, int] = {}

    def increment(self, metric: str, amount: int = 1) -> None:
        self._counters[metric] = self._counters.get(metric, 0) + amount

    def get_count(self, metric: str) -> int:
        return self._counters.get(metric, 0)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def record_latency(self, endpoint: str, latency_ms: float) -> None:
        self.latency_histogram.labels(endpoint=endpoint).observe(latency_ms)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
    def sanitize_path(self, raw_path: str) -> str:
        return re.sub(r'/\d+', '/:id', raw_path)
