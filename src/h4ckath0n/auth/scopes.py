"""Pure functional helpers for parsing, normalizing, and formatting scopes."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated string into a list of deduplicated, stripped scopes."""
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized, comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))


def normalize_scope_list(raw: str) -> str:
    """Normalize a comma-separated scopes string (strip, deduplicate, format)."""
    return format_scopes(raw.split(","))
