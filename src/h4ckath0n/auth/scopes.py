"""Scope normalization and parsing helpers."""

from __future__ import annotations

from collections.abc import Iterable


def iter_scopes(raw: str) -> Iterable[str]:
    """Iterate over a comma-separated string, stripping whitespace and removing empties."""
    return filter(None, map(str.strip, raw.split(",")))


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated string of scopes into a stable deduplicated list."""
    return list(dict.fromkeys(iter_scopes(raw)))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))
