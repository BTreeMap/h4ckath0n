"""Tests for auth scope parsing and serialization."""

from h4ckath0n.auth.scopes import parse_scopes, serialize_scopes


def test_parse_scopes_empty():
    assert parse_scopes("") == []
    assert parse_scopes("   ") == []


def test_parse_scopes_deduplicates_and_orders():
    assert parse_scopes("admin, demo, admin, test, demo") == ["admin", "demo", "test"]


def test_parse_scopes_strips_whitespace():
    assert parse_scopes("  admin  ,   demo  ") == ["admin", "demo"]


def test_serialize_scopes():
    assert serialize_scopes(["admin", "demo", "admin"]) == "admin,demo"
    assert serialize_scopes([]) == ""
