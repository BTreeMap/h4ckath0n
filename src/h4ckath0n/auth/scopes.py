"""Scope parsing and formatting utilities."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a list of cleaned, non-empty scopes."""
    return list(filter(None, map(str.strip, raw.split(","))))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a deduplicated, comma-separated string preserving order."""  # noqa: E501
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))
