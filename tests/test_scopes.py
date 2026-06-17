"""Tests for scope pure functions."""

from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes("") == []
    assert parse_scopes("  ") == []
    assert parse_scopes("foo") == ["foo"]
    assert parse_scopes("foo,bar") == ["foo", "bar"]
    assert parse_scopes(" foo , bar ,baz ") == ["foo", "bar", "baz"]
    assert parse_scopes("foo,,bar,") == ["foo", "bar"]
    assert parse_scopes("foo,bar,foo") == ["foo", "bar"]


def test_format_scopes() -> None:
    assert format_scopes([]) == ""
    assert format_scopes([""]) == ""
    assert format_scopes(["foo"]) == "foo"
    assert format_scopes(["foo", "bar"]) == "foo,bar"
    assert format_scopes([" foo ", "bar "]) == "foo,bar"
    assert format_scopes(["foo", "bar", "foo"]) == "foo,bar"
    assert format_scopes(["foo", "", "bar", None]) == "foo,bar"  # type: ignore[list-item]
