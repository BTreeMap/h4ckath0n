from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes():
    assert parse_scopes("a, b, c") == ["a", "b", "c"]
    assert parse_scopes("a,,b, , c") == ["a", "b", "c"]
    assert parse_scopes("a, a, b") == ["a", "b"]
    assert parse_scopes("") == []


def test_format_scopes():
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes(["a", " ", "b", "a"]) == "a,b"
    assert format_scopes([]) == ""
