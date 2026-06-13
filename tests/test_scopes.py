from h4ckath0n.auth.scopes import format_scopes, normalize_scopes, parse_scopes


def test_parse_scopes():
    assert parse_scopes("") == []
    assert parse_scopes(" a , b, c ,a ") == ["a", "b", "c"]
    assert parse_scopes("admin, demo,admin") == ["admin", "demo"]


def test_format_scopes():
    assert format_scopes(["a", " b ", "", "a"]) == "a,b"
    assert format_scopes([]) == ""


def test_normalize_scopes():
    assert normalize_scopes(" a , b, c ,a ") == "a,b,c"
    assert normalize_scopes("") == ""
