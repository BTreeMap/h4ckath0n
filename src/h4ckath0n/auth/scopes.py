"""Scope normalization and parsing helpers."""

from __future__ import annotations


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated string of scopes into a stable deduplicated list."""
    parts = filter(None, map(str.strip, raw.split(",")))
    # de-duplicate preserving order
    return list(dict.fromkeys(parts))


def normalize_scopes(raw: str) -> str:
    """Normalize a comma-separated string of scopes."""
    return ",".join(parse_scopes(raw))
