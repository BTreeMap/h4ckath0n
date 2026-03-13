"""Scope processing and normalization utilities.

Provides functional pipelines for consistently parsing, formatting, and normalizing
authorization scopes throughout the application.
"""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a clean list.

    Whitespace is trimmed, empty elements are removed, and duplicates
    are eliminated while preserving order.
    """
    clean_parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(clean_parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a clean comma-separated string.

    Whitespace is trimmed, empty elements are removed, and duplicates
    are eliminated while preserving order.
    """
    clean_parts = filter(None, map(str.strip, scopes))
    return ",".join(dict.fromkeys(clean_parts))


def normalize_scopes_string(raw: str) -> str:
    """Normalize a comma-separated scopes string into a clean comma-separated string.

    Whitespace is trimmed, empty elements are removed, and duplicates
    are eliminated while preserving order.
    """
    return format_scopes(raw.split(","))
