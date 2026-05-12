"""Pure helpers for authentication scopes."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list, preserving order."""
    parts = filter(None, (s.strip() for s in raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    parts = filter(None, (s.strip() for s in scopes if s))
    return ",".join(dict.fromkeys(parts))


def normalize_scope_list(raw: str) -> str:
    """Normalize a comma-separated scopes string.

    Trims whitespace, deduplicates, and preserves order.
    """
    return format_scopes(parse_scopes(raw))
