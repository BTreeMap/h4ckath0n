"""Pure helper utilities for scope string normalization and parsing."""

from __future__ import annotations

from collections.abc import Iterable


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated string into a deduplicated list of trimmed scopes.

    Preserves order.
    """
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Iterable[str]) -> str:
    """Format an iterable of scopes into a comma-separated string.

    Trims and deduplicates values.
    """
    parts = filter(None, (s.strip() for s in scopes if s))
    return ",".join(dict.fromkeys(parts))
