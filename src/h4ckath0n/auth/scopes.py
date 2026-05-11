"""Pure helpers for handling user scopes."""

from __future__ import annotations

from collections.abc import Iterable


def normalize_scope_list(scopes: Iterable[str | None]) -> list[str]:
    """Normalize a list of scopes.

    Strips whitespace, removes empty strings and None values,
    and deduplicates while preserving order.
    """
    valid_scopes = filter(None, scopes)
    parts = filter(None, map(str.strip, valid_scopes))
    return list(dict.fromkeys(parts))


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a normalized list of scopes."""
    return normalize_scope_list(raw.split(","))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    return ",".join(normalize_scope_list(scopes))
