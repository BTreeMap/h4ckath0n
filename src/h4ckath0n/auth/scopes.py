"""Functional utilities for processing comma-separated scope strings."""

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """
    Parse a comma-separated string of scopes into a stable, deduplicated list.
    Empty strings and whitespace are stripped.
    """
    parts = filter(None, map(str.strip, raw.split(",")))
    # de-duplicate preserving order
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """
    Format an iterable of scopes into a comma-separated string.
    Empty strings and whitespace are stripped. Order is preserved.
    """
    parts = filter(None, map(str.strip, scopes))
    # de-duplicate preserving order
    return ",".join(dict.fromkeys(parts))
