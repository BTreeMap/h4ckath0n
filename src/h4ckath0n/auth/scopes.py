"""Pure functional helpers for parsing and formatting comma-separated scope strings."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a list of normalized scopes.

    Removes whitespace and empty entries. Preserves order.
    """
    if not raw:
        return []
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string.

    Removes whitespace and empty entries. Preserves order.
    """
    parts = filter(None, map(str.strip, scopes))
    return ",".join(dict.fromkeys(parts))


def add_scopes(raw: str, new_scopes: Iterable[str]) -> str:
    """Add new scopes to an existing comma-separated scopes string."""
    existing = parse_scopes(raw)
    to_add = parse_scopes(format_scopes(new_scopes))

    # Append new scopes that aren't already present
    for scope in to_add:
        if scope not in existing:
            existing.append(scope)

    return format_scopes(existing)


def remove_scopes(raw: str, scopes_to_remove: Iterable[str]) -> str:
    """Remove scopes from an existing comma-separated scopes string."""
    existing = parse_scopes(raw)
    to_remove = set(parse_scopes(format_scopes(scopes_to_remove)))

    remaining = [s for s in existing if s not in to_remove]
    return format_scopes(remaining)
