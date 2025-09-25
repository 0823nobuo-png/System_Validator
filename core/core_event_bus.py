"""
System Validator / Theaterverse Final
Core Event Bus - Pub/Sub messaging system

Provides a central event dispatch mechanism. Supports synchronous and
asynchronous subscribers. Used by kernel and plugins for decoupled
communication.
"""

import asyncio
import logging
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], Any]]] = {}

    def subscribe(self, event: str, handler: Callable[[Any], Any]):
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(handler)
        logger.debug("Subscribed handler %s to event '%s'", handler, event)

    def emit(self, event: str, payload: Any = None):
        handlers = self._subscribers.get(event, [])
        logger.debug("Emitting event '%s' to %d handlers", event, len(handlers))
        for handler in handlers:
            try:
                result = handler(payload)
                if asyncio.iscoroutine(result):
                    asyncio.create_task(result)
            except Exception as e:
                logger.exception("Error in handler for event '%s': %s", event, e)

    async def emit_async(self, event: str, payload: Any = None):
        handlers = self._subscribers.get(event, [])
        logger.debug(
            "Asynchronously emitting event '%s' to %d handlers", event, len(handlers)
        )
        for handler in handlers:
            try:
                result = handler(payload)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.exception("Error in async handler for event '%s': %s", event, e)


--- END OF STRUCTURE ---
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_event_bus.py
# /root/System_Validator/APP_DIR/theaterverse_final/core/core_event_bus.py
# --- END OF STRUCTURE ---
