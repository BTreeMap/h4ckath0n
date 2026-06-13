from h4ckath0n.auth.schemas import format_scopes, parse_scopes


def test_parse_scopes():
    assert parse_scopes(None) == []
    assert parse_scopes("") == []
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes(" a , b , c ") == ["a", "b", "c"]
    assert parse_scopes("a,b,a,c") == ["a", "b", "c"]
    assert parse_scopes("a,,b") == ["a", "b"]


def test_format_scopes():
    assert format_scopes([]) == ""
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes([" a ", " b ", " c "]) == "a,b,c"
    assert format_scopes(["a", "b", "a", "c"]) == "a,b,c"
    assert format_scopes(["a", "", "b"]) == "a,b"
