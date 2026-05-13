"""Tests for authorization scopes pure helpers."""

from h4ckath0n.auth.scopes import format_scopes, normalize_scope_list, parse_scopes


def test_parse_scopes() -> None:
    # empty
    assert parse_scopes("") == []
    assert parse_scopes("   ") == []
    assert parse_scopes(",, ,") == []

    # single
    assert parse_scopes("admin") == ["admin"]
    assert parse_scopes("  admin  ") == ["admin"]

    # multiple
    assert parse_scopes("admin,user") == ["admin", "user"]
    assert parse_scopes("admin, user , foo") == ["admin", "user", "foo"]

    # duplicates
    assert parse_scopes("admin,admin") == ["admin"]
    assert parse_scopes("admin, user, admin") == ["admin", "user"]

    # preserves order
    assert parse_scopes("z,a,c,b") == ["z", "a", "c", "b"]


def test_format_scopes() -> None:
    # empty
    assert format_scopes([]) == ""
    assert format_scopes(["", " "]) == ""

    # single
    assert format_scopes(["admin"]) == "admin"
    assert format_scopes([" admin "]) == "admin"

    # multiple
    assert format_scopes(["admin", "user"]) == "admin,user"
    assert format_scopes([" admin ", "user ", " foo"]) == "admin,user,foo"

    # duplicates
    assert format_scopes(["admin", "admin"]) == "admin"
    assert format_scopes(["admin", "user", "admin"]) == "admin,user"

    # preserves order
    assert format_scopes(["z", "a", "c", "b"]) == "z,a,c,b"


def test_normalize_scope_list() -> None:
    # empty
    assert normalize_scope_list("") == ""
    assert normalize_scope_list("   ") == ""
    assert normalize_scope_list(",, ,") == ""

    # single
    assert normalize_scope_list("admin") == "admin"
    assert normalize_scope_list("  admin  ") == "admin"

    # multiple
    assert normalize_scope_list("admin,user") == "admin,user"
    assert normalize_scope_list("admin, user , foo") == "admin,user,foo"

    # duplicates
    assert normalize_scope_list("admin,admin") == "admin"
    assert normalize_scope_list("admin, user, admin") == "admin,user"

    # preserves order
    assert normalize_scope_list("z,a,c,b") == "z,a,c,b"
