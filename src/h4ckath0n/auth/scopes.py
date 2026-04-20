"""Functional utilities for parsing and formatting scope strings."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(scopes_str: str) -> list[str]:
    """Parse a comma-separated scopes string into a list of normalized scopes.

    Preserves order and removes duplicates and empty strings.
    """
    parts = filter(None, map(str.strip, scopes_str.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    parts = filter(None, map(str.strip, scopes))
    return ",".join(dict.fromkeys(parts))
