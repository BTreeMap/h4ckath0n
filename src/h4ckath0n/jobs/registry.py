"""Job handler registry."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger(__name__)

# Type for job handlers - receives payload dict, returns result dict
JobHandler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]

_registry: dict[str, JobHandler] = {}
_internal_kinds: set[str] = set()


def register(kind: str, *, internal: bool = False) -> Callable[[JobHandler], JobHandler]:
    """Decorator to register a job handler.

    Parameters
    ----------
    kind:
        Unique handler name (e.g. ``"demo.echo"``).
    internal:
        When ``True`` the handler cannot be invoked from the public
        ``POST /jobs`` API – it is only callable from server-side code
        (e.g. the upload router enqueuing ``uploads.extract_text``).
    """

    def decorator(fn: JobHandler) -> JobHandler:
        _registry[kind] = fn
        if internal:
            _internal_kinds.add(kind)
        return fn

    return decorator


def get_handler(kind: str) -> JobHandler | None:
    return _registry.get(kind)


def registered_kinds() -> list[str]:
    """Return all registered handler kinds (public + internal)."""
    return list(_registry.keys())


def public_kinds() -> list[str]:
    """Return only handler kinds that may be invoked from the public API."""
    return [k for k in _registry if k not in _internal_kinds]


def is_internal(kind: str) -> bool:
    """Return whether a handler is internal-only."""
    return kind in _internal_kinds
