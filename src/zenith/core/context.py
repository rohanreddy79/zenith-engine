"""Execution context and cancellation tokens."""

import uuid
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ExecutionContext:
    context_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_cancelled: bool = False

    def copy(self) -> 'ExecutionContext':
        return ExecutionContext(
            context_id=str(uuid.uuid4()),
            trace_id=self.trace_id,
            metadata=self.metadata.copy(),
            is_cancelled=self.is_cancelled
        )
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
    def with_trace_id(self, trace_id: str) -> 'ExecutionContext':
        ctx = self.copy()
        ctx.trace_id = trace_id
        return ctx
