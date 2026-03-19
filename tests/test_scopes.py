from h4ckath0n.auth.scopes import parse_scopes, format_scopes

def test_parse_scopes():
    assert parse_scopes("") == []
    assert parse_scopes("   ") == []
    assert parse_scopes("a") == ["a"]
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes("a, b,  c  ") == ["a", "b", "c"]
    assert parse_scopes("a,,b, ,c") == ["a", "b", "c"]
    assert parse_scopes("a,b,a,c,b") == ["a", "b", "c"]

def test_format_scopes():
    assert format_scopes([]) == ""
    assert format_scopes(["a"]) == "a"
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes(["a ", " b", "  c  "]) == "a,b,c"
    assert format_scopes(["a", "", "b", " ", "c"]) == "a,b,c"
    assert format_scopes(["a", "b", "a", "c", "b"]) == "a,b,c"
