"""Scope parsing and formatting utilities."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> Iterable[str]:
    """Parse a comma-separated scopes string into an iterable of normalized scopes."""
    return filter(None, map(str.strip, raw.split(",")))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized, order-preserving comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))
