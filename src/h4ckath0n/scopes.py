"""Scope parsing and formatting utilities."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> Iterable[str]:
    """Parse a comma-separated scopes string into a clean iterable of scopes."""
    return filter(None, map(str.strip, raw.split(",")))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a deduplicated, comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))


def normalize_scopes(raw: str) -> str:
    """Normalize a comma-separated scopes string."""
    return format_scopes(raw.split(","))
