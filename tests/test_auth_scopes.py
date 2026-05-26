from __future__ import annotations

from h4ckath0n.auth.scopes import format_scopes, normalize_scope_list, parse_scopes


def test_normalize_scope_list() -> None:
    # Handles empty/null/whitespace inputs
    assert normalize_scope_list(["", "  ", None]) == []  # type: ignore

    # Strips whitespace
    assert normalize_scope_list(["  a  ", "b\n"]) == ["a", "b"]

    # Deduplicates while preserving order
    assert normalize_scope_list(["c", "a", "c", "b", "a"]) == ["c", "a", "b"]


def test_parse_scopes() -> None:
    # Handles empty and whitespace-only strings
    assert parse_scopes("") == []
    assert parse_scopes("   ") == []

    # Handles commas and whitespace
    assert parse_scopes("a, b ,c") == ["a", "b", "c"]

    # Handles trailing/leading commas and duplicates
    assert parse_scopes(",a,b,a,,c,") == ["a", "b", "c"]


def test_format_scopes() -> None:
    # Handles empty lists
    assert format_scopes([]) == ""

    # Normalizes, deduplicates, and formats correctly
    assert format_scopes([" c", "a ", "c", "", "b"]) == "c,a,b"
