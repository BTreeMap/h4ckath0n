"""Pure functional helpers for parsing and formatting user scopes."""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def iter_scopes(raw: str) -> Iterator[str]:
    """Yield normalized, non-empty scopes from a comma-separated string."""
    return filter(None, map(str.strip, raw.split(",")))


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list, preserving order."""
    return list(dict.fromkeys(iter_scopes(raw)))


def format_scopes(scopes: Iterable[str | None]) -> str:
    """Format an iterable of scopes into a deduplicated, comma-separated string."""
    return ",".join(dict.fromkeys(filter(None, map(lambda s: s.strip() if s else None, scopes))))


def normalize_scopes(raw: str) -> str:
    """Normalize a comma-separated scopes string (trim, deduplicate, preserve order)."""
    return ",".join(dict.fromkeys(iter_scopes(raw)))
