from h4ckath0n.auth.scopes import format_scopes, iter_scopes, normalize_scopes, parse_scopes


def test_iter_scopes() -> None:
    assert list(iter_scopes("")) == []
    assert list(iter_scopes("a,b,c")) == ["a", "b", "c"]
    assert list(iter_scopes(" a , b , c ")) == ["a", "b", "c"]
    assert list(iter_scopes("a,,c")) == ["a", "c"]


def test_parse_scopes() -> None:
    assert parse_scopes("") == []
    assert parse_scopes("a,b,c") == ["a", "b", "c"]
    assert parse_scopes("a,b,a,c") == ["a", "b", "c"]


def test_format_scopes() -> None:
    assert format_scopes(["a", "b", "c"]) == "a,b,c"
    assert format_scopes(["a", "b", "a"]) == "a,b"
    assert format_scopes("a") == "a"
    assert format_scopes([" a ", "b"]) == "a,b"
    assert format_scopes([]) == ""


def test_normalize_scopes() -> None:
    assert normalize_scopes("") == ""
    assert normalize_scopes(" a , b , c ") == "a,b,c"
    assert normalize_scopes("a,b,a,c") == "a,b,c"
    assert normalize_scopes(",a,,b,") == "a,b"
