from h4ckath0n.auth.scopes import normalize_scopes, parse_scopes


def test_parse_scopes() -> None:
    assert parse_scopes("") == []
    assert parse_scopes(",") == []
    assert parse_scopes(" , ") == []
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes(" a , b , c ") == ["a", "b", "c"]
    assert parse_scopes("a,,b,c") == ["a", "b", "c"]
    assert parse_scopes("a,b,b,c") == ["a", "b", "c"]
    assert parse_scopes("c,b,a,b,c") == ["c", "b", "a"]


def test_normalize_scopes() -> None:
    assert normalize_scopes("") == ""
    assert normalize_scopes(",") == ""
    assert normalize_scopes(" , ") == ""
    assert normalize_scopes("a,b,c") == "a,b,c"
    assert normalize_scopes(" a , b , c ") == "a,b,c"
    assert normalize_scopes("a,,b,c") == "a,b,c"
    assert normalize_scopes("a,b,b,c") == "a,b,c"
    assert normalize_scopes("c,b,a,b,c") == "c,b,a"
