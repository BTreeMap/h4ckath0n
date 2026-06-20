"""Convenience wrappers for traced tools and graph nodes."""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, Protocol, TypeVar, cast

from h4ckath0n.obs.redaction import redact_value

R = TypeVar("R", covariant=True)


class TracedCallable(Protocol[R]):
    """A callable that carries tracing metadata as a discoverable attribute."""

    __trace_meta__: dict[str, Any]

    def __call__(self, *args: Any, **kwargs: Any) -> R: ...


def traced_tool(
    fn: Callable[..., R],
    *,
    name: str | None = None,
    redact: bool = False,
) -> TracedCallable[R]:
    """Wrap *fn* with metadata suitable for tracing frameworks.

    When *redact* is ``True``, string keyword arguments are passed through the
    default redactor before being forwarded to *fn*.
    """
    tool_name = name if name is not None else str(getattr(fn, "__name__", "tool"))

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> R:
        if redact:
            kwargs = {k: redact_value(v) if isinstance(v, str) else v for k, v in kwargs.items()}
        return fn(*args, **kwargs)

    wrapper.__name__ = tool_name
    traced = cast(TracedCallable[R], wrapper)
    traced.__trace_meta__ = {"tool_name": tool_name}
    return traced


def traced_node(
    fn: Callable[..., R],
    *,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
    redact: bool = False,
) -> TracedCallable[R]:
    """Wrap *fn* with metadata suitable for LangGraph node tracing."""
    node_name = name if name is not None else str(getattr(fn, "__name__", "node"))
    meta = metadata or {}

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> R:
        if redact:
            kwargs = {k: redact_value(v) if isinstance(v, str) else v for k, v in kwargs.items()}
        return fn(*args, **kwargs)

    wrapper.__name__ = node_name
    traced = cast(TracedCallable[R], wrapper)
    traced.__trace_meta__ = {"node_name": node_name, **meta}
    return traced
