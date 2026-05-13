"""Pure helpers for parsing, validating, and formatting authorization scopes."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated string into a list of scopes.

    Whitespace is trimmed and duplicates are removed, preserving order.
    Empty segments are ignored.
    """
    if not raw:
        return []
    return list(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a comma-separated string.

    Whitespace is trimmed and duplicates are removed, preserving order.
    Empty segments are ignored.
    """
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))


def normalize_scope_list(raw: str) -> str:
    """Normalize a comma-separated scopes string.

    Whitespace is trimmed and duplicates are removed, preserving order.
    Empty segments are ignored.
    """
    return format_scopes(parse_scopes(raw))
