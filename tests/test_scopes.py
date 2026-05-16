
from h4ckath0n.auth.scopes import format_scopes, normalize_scope_list, parse_scopes


def test_parse_scopes():
    assert parse_scopes("foo,bar") == ["foo", "bar"]
    assert parse_scopes("foo, bar,  baz") == ["foo", "bar", "baz"]
    assert parse_scopes("foo,,bar") == ["foo", "bar"]
    assert parse_scopes("  ") == []
    assert parse_scopes(None) == []
    assert parse_scopes("foo,bar,foo") == ["foo", "bar"]


def test_normalize_scope_list():
    assert normalize_scope_list(["foo", "bar"]) == ["foo", "bar"]
    assert normalize_scope_list(["foo", " bar ", "baz"]) == ["foo", "bar", "baz"]
    assert normalize_scope_list(["foo", "", "bar"]) == ["foo", "bar"]
    assert normalize_scope_list([]) == []
    assert normalize_scope_list(["foo", "bar", "foo"]) == ["foo", "bar"]


def test_format_scopes():
    assert format_scopes(["foo", "bar"]) == "foo,bar"
    assert format_scopes(["foo", " bar ", "baz"]) == "foo,bar,baz"
    assert format_scopes(["foo", "", "bar"]) == "foo,bar"
    assert format_scopes([]) == ""
    assert format_scopes(["foo", "bar", "foo"]) == "foo,bar"
