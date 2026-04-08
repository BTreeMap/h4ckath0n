from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes("foo,bar") == ["foo", "bar"]
    assert parse_scopes(" foo , bar ") == ["foo", "bar"]
    assert parse_scopes("foo,,bar,foo") == ["foo", "bar"]
    assert parse_scopes("") == []


def test_format_scopes() -> None:
    assert format_scopes(["foo", "bar"]) == "foo,bar"
    assert format_scopes(["foo ", " bar"]) == "foo,bar"
    assert format_scopes(["foo", "", "bar", "foo"]) == "foo,bar"
    assert format_scopes([]) == ""
