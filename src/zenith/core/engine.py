"""Core execution engine and priority worker pool scheduler."""

import asyncio
import threading
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class EngineConfig:
    max_workers: int = 16
    queue_capacity: int = 10000
    scale_threshold: int = 500
    heartbeat_interval: float = 1.0


class Task:
    def __init__(self, task_id: str, fn: Callable, *args, priority: int = 0, **kwargs):
        self.task_id = task_id
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.priority = priority
        self.future: asyncio.Future = asyncio.Future()
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True
        if not self.future.done():
            self.future.cancel()


class AsyncEngine:
    def __init__(self, config: Optional[EngineConfig] = None):
        self.config = config or EngineConfig()
        self._active_tasks: Dict[str, Task] = {}
        self._lock = threading.Lock()
        self._running = False

    async def start(self) -> None:
        self._running = True

    async def shutdown(self) -> None:
        self._running = False
        with self._lock:
            for task in self._active_tasks.values():
                task.cancel()

    async def submit(self, fn: Callable, *args, **kwargs) -> Any:
        task_id = f"task-{len(self._active_tasks) + 1}"
        task = Task(task_id, fn, *args, **kwargs)
        with self._lock:
            self._active_tasks[task_id] = task
        # Execute task
        try:
            if asyncio.iscoroutinefunction(fn):
                res = await fn(*args, **kwargs)
            else:
                res = fn(*args, **kwargs)
            task.future.set_result(res)
            return res
        except Exception as exc:
            task.future.set_exception(exc)
            raise
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    @property
    def supervisor(self) -> 'WorkerSupervisor':
        return self._supervisor
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def auto_scale_workers(self, queue_depth: int) -> None:
        if queue_depth > self.config.scale_threshold:
            self._worker_pool.grow(delta=4)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def cancel_task(self, task_id: str) -> bool:
        with self._lock:
            if task_id in self._active_tasks:
                self._active_tasks[task_id].cancel()
                return True
            return False
    def schedule_priority(self, task: 'Task', priority: int = 1) -> str:
        """Schedule high-priority task with preemptive queue placement."""
        return self._scheduler.enqueue_priority(task, priority)
    def _fast_dispatch(self) -> None:
        # Lock-free batch dispatch to minimize GIL contention
        tasks = self._ring_buffer.drain_batch(max_items=64)
        for task in tasks:
            self._worker_pool.submit_nowait(task)
