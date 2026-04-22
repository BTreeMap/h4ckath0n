"""Pure helpers for normalizing and parsing scopes."""

from collections.abc import Iterable


def iter_scopes(raw: str | Iterable[str]) -> Iterable[str]:
    """Yield normalized, deduplicated scopes, preserving order."""
    if isinstance(raw, str):
        raw = raw.split(",")
    return dict.fromkeys(filter(None, map(str.strip, raw)))


def parse_scopes(raw: str | Iterable[str]) -> list[str]:
    """Parse and normalize scopes into a deduplicated list."""
    return list(iter_scopes(raw))


def format_scopes(raw: str | Iterable[str]) -> str:
    """Format scopes into a normalized comma-separated string."""
    return ",".join(iter_scopes(raw))
