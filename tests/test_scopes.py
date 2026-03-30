from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes():
    assert parse_scopes("") == []
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes(" a , b , a , c ") == ["a", "b", "c"]
    assert parse_scopes("a,,b,,") == ["a", "b"]


def test_format_scopes():
    assert format_scopes([]) == ""
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes([" a ", "b", "a", "c"]) == "a,b,c"
    assert format_scopes(["a,b", "c", "d,a"]) == "a,b,c,d"
    assert format_scopes(["a,,b", ""]) == "a,b"
