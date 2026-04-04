from __future__ import annotations

from collections.abc import Iterable


def iter_scopes(raw: str) -> Iterable[str]:
    """Yield normalized scopes from a comma-separated string."""
    if not raw:
        return iter([])
    return filter(None, map(str.strip, raw.split(",")))


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated string into a deduplicated list of scopes preserving order."""
    return list(dict.fromkeys(iter_scopes(raw)))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a deduplicated comma-separated string preserving order."""
    if isinstance(scopes, str):
        scopes = [scopes]
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))


def normalize_scopes(raw: str) -> str:
    """Normalize a comma-separated scopes string, deduplicating and preserving order."""
    return format_scopes(iter_scopes(raw))
