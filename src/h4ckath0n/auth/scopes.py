"""Pure helpers for parsing and formatting comma-separated scope strings."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list, preserving order."""
    if not raw:
        return []
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a comma-separated string, deduplicating and preserving."""
    parts = filter(None, map(lambda x: str.strip(x) if x is not None else "", scopes))
    return ",".join(dict.fromkeys(parts))
