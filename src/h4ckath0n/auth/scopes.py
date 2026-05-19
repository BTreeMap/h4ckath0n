"""Pure helpers for parsing, formatting, and normalizing authentication scopes."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list of strings."""
    if not raw:
        return []
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))


def normalize_scope_list(raw: str) -> str:
    """Normalize a comma-separated scopes string (deduplicate, strip whitespace)."""
    return format_scopes(parse_scopes(raw))
