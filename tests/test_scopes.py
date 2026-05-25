from h4ckath0n.auth.scopes import format_scopes, normalize_scope_list, parse_scopes


def test_parse_scopes():
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes(" a , b , c ") == ["a", "b", "c"]
    assert parse_scopes("a,,b,,") == ["a", "b"]
    assert parse_scopes("a,b,a") == ["a", "b", "a"]
    assert parse_scopes("") == []


def test_normalize_scope_list():
    assert normalize_scope_list(["a", "b", "c"]) == ["a", "b", "c"]
    assert normalize_scope_list(["a", "b", "a"]) == ["a", "b"]
    assert normalize_scope_list([" a ", "b", " c ", ""]) == ["a", "b", "c"]
    assert normalize_scope_list([]) == []


def test_format_scopes():
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes(["a", "b", "a"]) == "a,b"
    assert format_scopes([" a ", "b", " c ", ""]) == "a,b,c"
    assert format_scopes([]) == ""
    assert format_scopes(parse_scopes("a, b, a")) == "a,b"
