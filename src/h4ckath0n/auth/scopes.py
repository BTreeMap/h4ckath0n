"""Scope parsing and formatting utilities."""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def iter_scopes(raw: str) -> Iterator[str]:
    """Yield deduplicated, stripped scopes from a comma-separated string."""
    return iter(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list of scopes."""
    return list(iter_scopes(raw))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))
