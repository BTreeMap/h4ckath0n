"""Pure functions for parsing and formatting user scopes."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str | None) -> list[str]:
    """Parse a comma-separated string of scopes into a clean list.

    Strips whitespace and drops empty values. Preserves order but does not deduplicate.
    """
    if not raw:
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string.

    Strips whitespace, drops empty values, and deduplicates while preserving order.
    """
    cleaned = (s.strip() for s in scopes if s.strip())
    return ",".join(dict.fromkeys(cleaned))
