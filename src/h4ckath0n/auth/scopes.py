"""Scope string parsing and formatting utilities."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a list of cleaned strings.

    Splits by comma, strips whitespace, and filters out empty strings.
    """
    return [s for s in map(str.strip, raw.split(",")) if s]


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string.

    Deduplicates scopes while preserving order, and joins them by comma.
    """
    cleaned = (s.strip() for s in scopes if s.strip())
    # Deduplicate preserving order
    return ",".join(dict.fromkeys(cleaned))
