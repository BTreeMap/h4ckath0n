"""Utilities for processing authorization scopes."""

from __future__ import annotations


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a list of normalized scopes."""
    return list(filter(None, map(str.strip, raw.split(","))))


def format_scopes(scopes: list[str]) -> str:
    """Format an iterable of scopes into a normalized, order-preserving comma-separated string."""
    parts = filter(None, map(str.strip, scopes))
    return ",".join(dict.fromkeys(parts))
