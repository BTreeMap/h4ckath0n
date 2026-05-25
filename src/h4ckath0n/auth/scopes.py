"""Pure helpers for parsing, validating, and formatting user authentication scopes."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """
    Parse a comma-separated scopes string into a list of individual scopes.
    Strips whitespace and removes empty segments. Does not deduplicate.
    """
    if not raw:
        return []
    return [s.strip() for s in raw.split(",") if s.strip()]


def normalize_scope_list(scopes: Iterable[str]) -> list[str]:
    """
    Normalize an iterable of scopes by stripping whitespace,
    removing empties, and deduplicating while preserving order.
    """
    return list(dict.fromkeys(s.strip() for s in scopes if s.strip()))


def format_scopes(scopes: Iterable[str]) -> str:
    """
    Format an iterable of scopes into a normalized, comma-separated string
    suitable for database storage or transmission.
    """
    return ",".join(normalize_scope_list(scopes))
