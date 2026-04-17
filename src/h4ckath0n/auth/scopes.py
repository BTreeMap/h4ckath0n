"""Scope parsing and normalization utilities."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into an ordered, deduplicated list."""
    return list(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    return ",".join(scopes)
