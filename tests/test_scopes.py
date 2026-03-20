"""Tests for scope parsing and formatting."""

from __future__ import annotations

from h4ckath0n.auth.scopes import format_scopes, parse_scopes


class TestParseScopes:
    def test_basic(self):
        assert parse_scopes("a,b,c") == ["a", "b", "c"]

    def test_with_whitespace(self):
        assert parse_scopes(" a , b , c ") == ["a", "b", "c"]

    def test_empty_parts(self):
        assert parse_scopes("a,,b,,c") == ["a", "b", "c"]

    def test_empty_string(self):
        assert parse_scopes("") == []

    def test_whitespace_only(self):
        assert parse_scopes("  ,  ,  ") == []


class TestFormatScopes:
    def test_basic(self):
        assert format_scopes(["a", "b", "c"]) == "a,b,c"

    def test_with_whitespace(self):
        assert format_scopes([" a ", " b ", " c "]) == "a,b,c"

    def test_empty_parts(self):
        assert format_scopes(["a", "", "b", "  ", "c"]) == "a,b,c"

    def test_deduplication(self):
        assert format_scopes(["a", "b", "a", "c", "b"]) == "a,b,c"

    def test_empty_iterable(self):
        assert format_scopes([]) == ""

    def test_generator(self):
        assert format_scopes(x for x in ["a", "b", "c"]) == "a,b,c"
