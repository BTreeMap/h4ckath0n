"""Scope parsing and normalization helpers."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a list of cleaned scopes."""
    return list(filter(None, map(str.strip, raw.split(","))))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized, order-preserving comma-separated string."""
    parts = filter(None, (s.strip() for s in scopes if s is not None))
    return ",".join(dict.fromkeys(parts))


def normalize_scopes(raw: str) -> str:
    """Normalize a comma-separated scopes string, deduplicating and preserving order."""
    return format_scopes(parse_scopes(raw))
