"""Helpers for parsing and serializing user scopes."""

from __future__ import annotations


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated, ordered list."""
    if not raw:
        return []
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def serialize_scopes(scopes: list[str]) -> str:
    """Serialize a list of scopes into a comma-separated string."""
    return ",".join(parse_scopes(",".join(scopes)))
