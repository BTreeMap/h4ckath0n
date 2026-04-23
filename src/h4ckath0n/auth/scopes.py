"""Centralized parsing and formatting for comma-separated scope strings."""

from collections.abc import Iterable


def parse_scopes(raw: str | None) -> list[str]:
    """
    Parse a comma-separated scopes string into a deduplicated list, preserving order.

    Empty, None, and whitespace-only segments are ignored.
    """
    if not raw:
        return []
    return list(dict.fromkeys(s for s in (x.strip() for x in raw.split(",")) if s))


def format_scopes(scopes: Iterable[str] | None) -> str:
    """
    Format an iterable of scopes into a normalized comma-separated string.

    Empty, None, and whitespace-only segments are ignored. Deduplicates preserving order.
    """
    if not scopes:
        return ""
    return ",".join(dict.fromkeys(s for s in (x.strip() for x in scopes) if s))
