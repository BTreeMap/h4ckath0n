"""Pure helpers for scope normalization, parsing, and formatting.

This module centralizes the string transformations for user scopes,
which are stored as comma-separated strings in the database.
"""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list of trimmed scopes.

    Order is preserved based on first occurrence.
    """
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    return ",".join(normalize_scope_list(scopes))


def normalize_scope_list(scopes: Iterable[str]) -> list[str]:
    """Normalize an iterable of scopes by trimming and deduplicating."""
    parts = filter(None, map(str.strip, scopes))
    return list(dict.fromkeys(parts))
