"""Tests for auth scopes utilities."""

from __future__ import annotations

from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes("") == []
    assert parse_scopes("  ") == []
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes(" a , b , c ") == ["a", "b", "c"]
    assert parse_scopes("a,b,a,c,b") == ["a", "b", "c"]
    assert parse_scopes("a,,b,,c") == ["a", "b", "c"]


def test_format_scopes() -> None:
    assert format_scopes([]) == ""
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes([" a ", "b ", " c"]) == "a,b,c"
    assert format_scopes(["a", "b", "a", "c", "b"]) == "a,b,c"
    assert format_scopes(["a", "", "b", None, "c"]) == "a,b,c"  # type: ignore
