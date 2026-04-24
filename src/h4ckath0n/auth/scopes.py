"""Scope parsing and normalization pipelines."""

from __future__ import annotations

from collections.abc import Iterable, Iterator


def parse_scopes(raw: str) -> Iterator[str]:
    """Parse a comma-separated scopes string into an iterator of clean scopes."""
    return filter(None, map(str.strip, raw.split(",")))


def normalize_scopes(raw: str | Iterable[str]) -> str:
    """
    Normalize a scope string or iterable into a clean, comma-separated string.
    De-duplicates while preserving order.
    """
    parts = parse_scopes(raw) if isinstance(raw, str) else filter(None, map(str.strip, raw))
    return ",".join(dict.fromkeys(parts))


def list_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a list of clean scopes."""
    return list(parse_scopes(raw))
