"""Tests for centralized scope parsing and formatting helpers."""

from h4ckath0n.auth.scopes import add_scopes, format_scopes, parse_scopes, remove_scopes


def test_parse_scopes():
    assert parse_scopes("") == []
    assert parse_scopes("foo") == ["foo"]
    assert parse_scopes("foo,bar") == ["foo", "bar"]
    assert parse_scopes(" foo , bar ") == ["foo", "bar"]
    assert parse_scopes("foo,,bar") == ["foo", "bar"]
    assert parse_scopes("foo,bar,foo") == ["foo", "bar"]


def test_format_scopes():
    assert format_scopes([]) == ""
    assert format_scopes(["foo"]) == "foo"
    assert format_scopes(["foo", "bar"]) == "foo,bar"
    assert format_scopes([" foo ", " bar "]) == "foo,bar"
    assert format_scopes(["foo", "", "bar"]) == "foo,bar"
    assert format_scopes(["foo", "bar", "foo"]) == "foo,bar"


def test_add_scopes():
    assert add_scopes("", ["foo"]) == "foo"
    assert add_scopes("foo", ["bar"]) == "foo,bar"
    assert add_scopes("foo,bar", ["baz"]) == "foo,bar,baz"
    assert add_scopes("foo", ["foo", "bar"]) == "foo,bar"
    assert add_scopes("foo,bar", ["foo"]) == "foo,bar"


def test_remove_scopes():
    assert remove_scopes("", ["foo"]) == ""
    assert remove_scopes("foo", ["foo"]) == ""
    assert remove_scopes("foo,bar", ["foo"]) == "bar"
    assert remove_scopes("foo,bar,baz", ["foo", "baz"]) == "bar"
    assert remove_scopes("foo,bar", ["baz"]) == "foo,bar"
