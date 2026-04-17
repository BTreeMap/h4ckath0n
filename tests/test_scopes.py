from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes("") == []
    assert parse_scopes(None) == []
    assert parse_scopes("foo,bar") == ["foo", "bar"]
    assert parse_scopes("foo, bar , baz") == ["foo", "bar", "baz"]
    assert parse_scopes("foo,,bar") == ["foo", "bar"]
    assert parse_scopes("  ,,  ") == []
    assert parse_scopes("a, a, b") == ["a", "a", "b"]


def test_format_scopes() -> None:
    assert format_scopes([]) == ""
    assert format_scopes(["foo", "bar"]) == "foo,bar"
    assert format_scopes(["foo", " bar ", "baz"]) == "foo,bar,baz"
    assert format_scopes(["foo", "", "bar"]) == "foo,bar"
    assert format_scopes(["  ", "  "]) == ""
    assert format_scopes(["a", "a", "b"]) == "a,b"
    assert format_scopes(["a", "b", "a"]) == "a,b"
