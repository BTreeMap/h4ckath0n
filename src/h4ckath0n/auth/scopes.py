"""Scope normalization and parsing helpers."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str | None) -> list[str]:
    """Parse a comma-separated string of scopes into a clean list.

    Whitespace is trimmed, empty scopes are discarded, and duplicates are removed
    while preserving the original order.
    """
    if not raw:
        return []
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def normalize_scope_list(scopes: Iterable[str]) -> list[str]:
    """Normalize an iterable of scope strings into a clean list.

    Whitespace is trimmed, empty scopes are discarded, and duplicates are removed
    while preserving the original order.
    """
    parts = filter(None, map(str.strip, scopes))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scope strings into a clean comma-separated string.

    Whitespace is trimmed, empty scopes are discarded, and duplicates are removed.
    """
    return ",".join(normalize_scope_list(scopes))
