"""Pure functional helpers for scope serialization and deduplication."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str | None) -> list[str]:
    """Parse a comma-separated scopes string into an ordered, deduplicated list."""
    if not raw:
        return []
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into an ordered, deduplicated comma-separated string."""
    parts = filter(None, map(str.strip, scopes))
    return ",".join(dict.fromkeys(parts))
