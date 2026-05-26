"""Pure functional helpers for parsing, validating, and formatting scopes."""

from __future__ import annotations

from collections.abc import Iterable


def normalize_scope_list(scopes: Iterable[str]) -> list[str]:
    """
    Clean and deduplicate a sequence of scope strings, preserving order.
    Whitespace is stripped, and empty strings are ignored.
    """
    parts = filter(None, (s.strip() for s in scopes if s is not None))
    return list(dict.fromkeys(parts))


def parse_scopes(raw: str) -> list[str]:
    """
    Parse a comma-separated scopes string into a cleaned list.
    """
    return normalize_scope_list(raw.split(","))


def format_scopes(scopes: Iterable[str]) -> str:
    """
    Format an iterable of scope strings into a normalized comma-separated string.
    """
    return ",".join(normalize_scope_list(scopes))
