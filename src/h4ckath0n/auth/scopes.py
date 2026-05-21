"""Centralized functional helpers for user scopes.

These pure functions ensure consistent whitespace trimming and deduplication
when working with scopes strings throughout the application.
"""

from __future__ import annotations

from collections.abc import Iterable


def normalize_scope_list(scopes: Iterable[str]) -> list[str]:
    """Return a deduplicated list of non-empty scope strings, preserving order."""
    parts = filter(None, map(str.strip, scopes))
    return list(dict.fromkeys(parts))


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a normalized list."""
    return normalize_scope_list(raw.split(","))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    return ",".join(normalize_scope_list(scopes))
