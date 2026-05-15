"""Centralized parsing, deduplication, and formatting of authentication scopes."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list of trimmed scopes."""
    return list(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))


def normalize_scope_list(raw: str) -> str:
    """Normalize a comma-separated scopes string.

    Trims whitespace, removes empty segments, and deduplicates elements while preserving order.
    """
    return format_scopes(parse_scopes(raw))
