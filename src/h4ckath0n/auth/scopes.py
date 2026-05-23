"""Centralized helpers for parsing, formatting, and normalizing authentication scopes."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """
    Parse a comma-separated scopes string into a deduplicated list,
    preserving order and removing empty/whitespace-only segments.
    """
    if not raw:
        return []
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """
    Format an iterable of scopes into a normalized comma-separated string,
    removing empty/whitespace-only segments and deduplicating while preserving order.
    """
    parts = filter(None, map(str.strip, scopes))
    return ",".join(dict.fromkeys(parts))


def normalize_scope_list(raw: str) -> str:
    """
    Normalize a comma-separated scopes string.
    """
    if not raw:
        return ""
    return format_scopes(raw.split(","))
