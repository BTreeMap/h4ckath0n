"""Scope normalization helpers."""

from __future__ import annotations


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list."""
    return list(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


def format_scopes(scopes: list[str]) -> str:
    """Format a list of scopes into a deduplicated comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))
