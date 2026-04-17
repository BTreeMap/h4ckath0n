from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes_empty():
    assert parse_scopes("") == []
    assert parse_scopes("   ") == []
    assert parse_scopes(",,") == []


def test_parse_scopes_whitespace():
    assert parse_scopes(" a , b  ,  c ") == ["a", "b", "c"]


def test_parse_scopes_deduplication():
    assert parse_scopes("a,b,a,c,b") == ["a", "b", "c"]


def test_parse_scopes_mixed():
    assert parse_scopes("  admin,  user ,,, admin, test ") == ["admin", "user", "test"]


def test_format_scopes():
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes([]) == ""
