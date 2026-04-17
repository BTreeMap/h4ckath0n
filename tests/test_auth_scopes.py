from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes() -> None:
    # Standard case
    assert parse_scopes("admin,user") == ["admin", "user"]
    # Whitespace handling
    assert parse_scopes(" admin ,  user  ") == ["admin", "user"]
    # Empty string
    assert parse_scopes("") == []
    # Extraneous commas and spaces
    assert parse_scopes("a,,b, c , ") == ["a", "b", "c"]
    # Order preserving deduplication
    assert parse_scopes("c,b,a,c,b") == ["c", "b", "a"]


def test_format_scopes() -> None:
    assert format_scopes(["admin", "user"]) == "admin,user"
    assert format_scopes([]) == ""
    assert format_scopes(["a"]) == "a"
