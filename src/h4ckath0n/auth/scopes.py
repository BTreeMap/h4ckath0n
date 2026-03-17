"""Scope normalization and formatting utilities."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list of scopes."""
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a comma-separated string."""
    return ",".join(scopes)


def normalize_scopes(raw: str) -> str:
    """Normalize a comma-separated scopes string (deduplicated, order-preserving)."""
    return format_scopes(parse_scopes(raw))
