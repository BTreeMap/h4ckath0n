"""Job handler registry."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger(__name__)

# Type for job handlers - receives payload dict, returns result dict
JobHandler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]

_registry: dict[str, JobHandler] = {}


def register(kind: str) -> Callable[[JobHandler], JobHandler]:
    """Decorator to register a job handler."""

    def decorator(fn: JobHandler) -> JobHandler:
        _registry[kind] = fn
        return fn

    return decorator


def get_handler(kind: str) -> JobHandler | None:
    return _registry.get(kind)


def registered_kinds() -> list[str]:
    return list(_registry.keys())
