"""Utilities for parsing and formatting comma-separated scopes."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str | None) -> list[str]:
    """Parse a comma-separated string into a deduplicated list of scopes, preserving order."""
    if not raw:
        return []
    return list(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a deduplicated comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))
