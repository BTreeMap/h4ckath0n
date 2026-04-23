from collections.abc import Iterable


def parse_scopes(raw: str | None) -> list[str]:
    if not raw:
        return []
    return list(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


def format_scopes(scopes: Iterable[str]) -> str:
    return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))


print(parse_scopes("foo, bar, foo, baz"))
print(format_scopes(["foo", "bar ", " foo", "baz", ""]))
