from collections.abc import Iterable


def parse_scopes(raw: str | None) -> list[str]:
    """Parse a comma-separated scopes string into an ordered, deduplicated list."""
    if not raw:
        return []
    return list(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


def format_scopes(scopes: Iterable[str] | str) -> str:
    """Format an iterable of scopes into a normalized comma-separated string."""
    if isinstance(scopes, str):
        scopes = [scopes]

    parts: list[str] = []
    for s in scopes:
        parts.extend(filter(None, map(str.strip, s.split(","))))
    return ",".join(dict.fromkeys(parts))
