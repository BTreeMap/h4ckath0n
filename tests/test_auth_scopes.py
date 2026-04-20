from __future__ import annotations

from h4ckath0n.auth.scopes import format_scopes, normalize_scopes_string, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes(" foo , bar, foo , , baz ") == ["foo", "bar", "baz"]
    assert parse_scopes("") == []
    assert parse_scopes("   ,  ") == []
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes("c,b,a,a,b,c") == ["c", "b", "a"]


def test_format_scopes() -> None:
    assert format_scopes([" foo ", "bar", "foo", "", "baz"]) == "foo,bar,baz"
    assert format_scopes(("a", "b", "c")) == "a,b,c"
    assert format_scopes([]) == ""
    assert format_scopes(["", "   "]) == ""
    assert format_scopes(["a", "b", "a"]) == "a,b"


def test_normalize_scopes_string() -> None:
    assert normalize_scopes_string(" foo , bar, foo , , baz ") == "foo,bar,baz"
    assert normalize_scopes_string("") == ""
    assert normalize_scopes_string("   ,  ") == ""
    assert normalize_scopes_string("a,b,c") == "a,b,c"
    assert normalize_scopes_string("c,b,a,a,b,c") == "c,b,a"
