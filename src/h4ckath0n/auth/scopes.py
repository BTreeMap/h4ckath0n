"""Functional utilities for processing scope strings."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list, preserving order."""
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    return ",".join(parse_scopes(",".join(scopes)))
