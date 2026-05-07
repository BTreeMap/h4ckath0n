"""Tests for authorization scope utilities."""

from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes():
    assert parse_scopes("") == []
    assert parse_scopes("  ") == []
    assert parse_scopes("a") == ["a"]
    assert parse_scopes("a,b") == ["a", "b"]
    assert parse_scopes(" a , b ") == ["a", "b"]
    assert parse_scopes("a,,b") == ["a", "b"]


def test_format_scopes():
    assert format_scopes([]) == ""
    assert format_scopes([""]) == ""
    assert format_scopes(["  "]) == ""
    assert format_scopes(["a"]) == "a"
    assert format_scopes(["a", "b"]) == "a,b"
    assert format_scopes([" a ", " b "]) == "a,b"
    assert format_scopes(["a", "", "b"]) == "a,b"
    assert format_scopes(["a", "b", "a"]) == "a,b"
