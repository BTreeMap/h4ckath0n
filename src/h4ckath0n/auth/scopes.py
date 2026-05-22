"""Pure functional helpers for parsing and normalizing scope lists."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str | None) -> list[str]:
    """Parse a comma-separated scope string into a deduplicated list of trimmed scopes."""
    if not raw:
        return []
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    parts = filter(None, map(str.strip, scopes))
    return ",".join(dict.fromkeys(parts))


def normalize_scope_list(raw: str | None) -> str:
    """Normalize a comma-separated scopes string."""
    if not raw:
        return ""
    return format_scopes(raw.split(","))
