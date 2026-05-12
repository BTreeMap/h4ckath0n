from h4ckath0n.auth.scopes import format_scopes, normalize_scope_list, parse_scopes


def test_parse_scopes():
    assert parse_scopes("") == []
    assert parse_scopes("admin,user") == ["admin", "user"]
    assert parse_scopes(" admin , user ") == ["admin", "user"]
    assert parse_scopes("admin,admin") == ["admin"]
    assert parse_scopes("admin,,user,") == ["admin", "user"]
    assert parse_scopes("b,a,c,a,b") == ["b", "a", "c"]


def test_format_scopes():
    assert format_scopes([]) == ""
    assert format_scopes(["admin", "user"]) == "admin,user"
    assert format_scopes([" admin ", " user "]) == "admin,user"
    assert format_scopes(["admin", "admin"]) == "admin"
    assert format_scopes(["admin", "", "user", None]) == "admin,user"  # type: ignore
    assert format_scopes(["b", "a", "c", "a", "b"]) == "b,a,c"


def test_normalize_scope_list():
    assert normalize_scope_list("") == ""
    assert normalize_scope_list("admin,user") == "admin,user"
    assert normalize_scope_list(" admin , user ") == "admin,user"
    assert normalize_scope_list("admin,admin") == "admin"
    assert normalize_scope_list("admin,,user,") == "admin,user"
    assert normalize_scope_list("b,a,c,a,b") == "b,a,c"
