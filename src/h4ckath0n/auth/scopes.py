"""Pure functional utilities for scope processing."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list, preserving order."""
    if not raw:
        return []
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scope strings into a normalized comma-separated string."""
    parts = filter(None, (p.strip() for s in scopes for p in s.split(",")))
    return ",".join(dict.fromkeys(parts))
