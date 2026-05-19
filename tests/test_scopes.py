from h4ckath0n.auth.scopes import format_scopes, normalize_scope_list, parse_scopes


def test_parse_scopes():
    assert parse_scopes("") == []
    assert parse_scopes("   ") == []
    assert parse_scopes("admin") == ["admin"]
    assert parse_scopes("admin, demo") == ["admin", "demo"]
    assert parse_scopes(" admin ,  demo  ") == ["admin", "demo"]
    assert parse_scopes("admin,demo,admin") == ["admin", "demo"]
    assert parse_scopes("admin,, ,demo") == ["admin", "demo"]


def test_format_scopes():
    assert format_scopes([]) == ""
    assert format_scopes(["admin"]) == "admin"
    assert format_scopes(["admin", "demo"]) == "admin,demo"
    assert format_scopes([" admin ", " demo "]) == "admin,demo"
    assert format_scopes(["admin", "demo", "admin"]) == "admin,demo"
    assert format_scopes(["admin", "", " ", "demo"]) == "admin,demo"


def test_normalize_scope_list():
    assert normalize_scope_list("") == ""
    assert normalize_scope_list("   ") == ""
    assert normalize_scope_list("admin") == "admin"
    assert normalize_scope_list("admin, demo") == "admin,demo"
    assert normalize_scope_list(" admin ,  demo  ") == "admin,demo"
    assert normalize_scope_list("admin,demo,admin") == "admin,demo"
    assert normalize_scope_list("admin,, ,demo") == "admin,demo"
