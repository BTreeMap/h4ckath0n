from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes("admin, demo,  demo  ") == ["admin", "demo"]
    assert parse_scopes("") == []
    assert parse_scopes("  ") == []
    assert parse_scopes(None) == []


def test_format_scopes() -> None:
    assert format_scopes("admin, demo,  demo  ") == "admin,demo"
    assert format_scopes(["admin, demo", "user"]) == "admin,demo,user"
    assert format_scopes(["  "]) == ""
