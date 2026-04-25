from h4ckath0n.auth.scopes import format_scopes, normalize_scopes, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes("") == []
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes("a, b, c") == ["a", "b", "c"]
    assert parse_scopes(" a , b , c ") == ["a", "b", "c"]
    assert parse_scopes("a,,b") == ["a", "b"]
    assert parse_scopes("a, a, b") == ["a", "a", "b"]


def test_format_scopes() -> None:
    assert format_scopes([]) == ""
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes(["a", "b", "a"]) == "a,b"
    assert format_scopes([" a ", "b", " c "]) == "a,b,c"
    assert format_scopes(["a", "", "b", None]) == "a,b"  # type: ignore


def test_normalize_scopes() -> None:
    assert normalize_scopes("") == ""
    assert normalize_scopes("a,b,c") == "a,b,c"
    assert normalize_scopes("a, b, c") == "a,b,c"
    assert normalize_scopes(" a , b , c ") == "a,b,c"
    assert normalize_scopes("a,a,b,c") == "a,b,c"
    assert normalize_scopes("a,,b") == "a,b"
