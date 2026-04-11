from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes():
    assert parse_scopes("") == []
    assert parse_scopes("admin") == ["admin"]
    assert parse_scopes("admin, demo") == ["admin", "demo"]
    assert parse_scopes("admin, , test, admin") == ["admin", "test"]


def test_format_scopes():
    assert format_scopes([]) == ""
    assert format_scopes(["admin"]) == "admin"
    assert format_scopes(["admin", "demo", ""]) == "admin,demo"
    assert format_scopes(["admin", " test ", "admin"]) == "admin,test"
