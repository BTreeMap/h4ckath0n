from h4ckath0n.auth.scopes import format_scopes, normalize_scope_list, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes("") == []
    assert parse_scopes("  ") == []
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes(" a , b , c ") == ["a", "b", "c"]
    assert parse_scopes("a,b,a,c") == ["a", "b", "c"]
    assert parse_scopes(",a,,b,") == ["a", "b"]


def test_format_scopes() -> None:
    assert format_scopes([]) == ""
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes([" a ", "b", "c"]) == "a,b,c"
    assert format_scopes(["a", "b", "a", "c"]) == "a,b,c"
    assert format_scopes(["a", "", "b"]) == "a,b"

    # Test with other iterables
    assert format_scopes(("a", "b")) == "a,b"
    assert format_scopes(set(["a", "b"])) in ["a,b", "b,a"]
    assert format_scopes(x for x in ["a", "b"]) == "a,b"


def test_normalize_scope_list() -> None:
    assert normalize_scope_list("") == ""
    assert normalize_scope_list("  ") == ""
    assert normalize_scope_list("a,b,c") == "a,b,c"
    assert normalize_scope_list(" a , b , c ") == "a,b,c"
    assert normalize_scope_list("a,b,a,c") == "a,b,c"
    assert normalize_scope_list(",a,,b,") == "a,b"
