"""Tests for scope parsing and formatting."""

from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes("") == []
    assert parse_scopes("   ") == []
    assert parse_scopes("admin,user") == ["admin", "user"]
    assert parse_scopes(" admin , user , admin ") == ["admin", "user"]
    assert parse_scopes("a,,b,") == ["a", "b"]


def test_format_scopes() -> None:
    assert format_scopes([]) == ""
    assert format_scopes(["admin", "user"]) == "admin,user"
    assert format_scopes([" admin ", "user", "admin"]) == "admin,user"
    assert format_scopes(["a", "", "b"]) == "a,b"
