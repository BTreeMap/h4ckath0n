"""Functional utilities for parsing and formatting scope strings."""

from collections.abc import Iterable


def parse_scopes(raw: str | None) -> tuple[str, ...]:
    """
    Parse a comma-separated scope string into a tuple of clean, unique scope names.
    Order is preserved based on first appearance.
    """
    if not raw:
        return ()
    parts = filter(None, map(str.strip, raw.split(",")))
    return tuple(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """
    Format an iterable of scopes into a clean, normalized comma-separated string.
    """
    parts = filter(None, map(str.strip, scopes))
    return ",".join(dict.fromkeys(parts))
