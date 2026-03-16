"""Scope normalization and validation utilities."""


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated list of scopes."""
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: list[str]) -> str:
    """Format a list of scopes into a comma-separated string."""
    return ",".join(scopes)
