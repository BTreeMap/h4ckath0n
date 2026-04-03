"""Scope parsing and formatting utilities."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list, preserving order."""
    return list(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized, comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))
