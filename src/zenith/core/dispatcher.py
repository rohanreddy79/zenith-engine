"""Event dispatcher and subscriber registry."""

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class EventEnvelope:
    topic: str
    payload: Any
    timestamp: float


class EventDispatcher:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger("zenith.dispatcher")

    def subscribe(self, topic: str, handler: Callable) -> None:
        self._handlers.setdefault(topic, []).append(handler)

    async def dispatch(self, event: EventEnvelope) -> None:
        handlers = self._handlers.get(event.topic, [])
        tasks = [h(event.payload) for h in handlers]
        if tasks:
            await asyncio.gather(*tasks)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    async def dispatch_safe(self, event: 'EventEnvelope') -> None:
        try:
            await self.dispatch(event)
        except Exception as err:
            self.logger.error('Event dispatch failed', exc_info=err)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
    def subscribe(self, topic: str, handler: 'EventHandler', filter_fn: Optional[Callable] = None) -> None:
        self._registry.add(topic, handler, filter_fn)
