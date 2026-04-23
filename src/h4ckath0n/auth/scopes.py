"""Scope parsing and formatting utilities."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated string of scopes into a clean list, preserving order."""
    if not raw:
        return []
    parts = filter(None, (s.strip() for s in raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized, comma-separated string."""
    parts = filter(None, (s.strip() for s in scopes if isinstance(s, str)))
    return ",".join(dict.fromkeys(parts))
