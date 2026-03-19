from collections.abc import Sequence


def parse_scopes(raw: str) -> list[str]:
    """Parse a comma-separated scopes string into a deduplicated, order-preserved list."""
    parts = filter(None, map(str.strip, raw.split(",")))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: Sequence[str]) -> str:
    """Format a sequence of scopes into a comma-separated string."""
    parts = filter(None, map(str.strip, scopes))
    return ",".join(dict.fromkeys(parts))
