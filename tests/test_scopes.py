"""Tests for scope utilities."""

from h4ckath0n.scopes import format_scopes, normalize_scopes, parse_scopes


def test_parse_scopes() -> None:
    assert list(parse_scopes("a, b, c")) == ["a", "b", "c"]
    assert list(parse_scopes("a, , c")) == ["a", "c"]
    assert list(parse_scopes("  a  ,b,  c  ")) == ["a", "b", "c"]
    assert list(parse_scopes("")) == []


def test_format_scopes() -> None:
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes(["a", "", "c"]) == "a,c"
    assert format_scopes(["  a  ", "b", "  c  "]) == "a,b,c"
    assert format_scopes(["a", "b", "a"]) == "a,b"
    assert format_scopes([]) == ""


def test_normalize_scopes() -> None:
    assert normalize_scopes("a, b, c") == "a,b,c"
    assert normalize_scopes("a, , c") == "a,c"
    assert normalize_scopes("  a  ,b,  c  ") == "a,b,c"
    assert normalize_scopes("a, b, a") == "a,b"
    assert normalize_scopes("") == ""
