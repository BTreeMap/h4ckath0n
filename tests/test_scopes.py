from h4ckath0n.auth.scopes import list_scopes, normalize_scopes, parse_scopes


def test_parse_scopes():
    assert list(parse_scopes("a,b,c")) == ["a", "b", "c"]
    assert list(parse_scopes(" a , b , c ")) == ["a", "b", "c"]
    assert list(parse_scopes("a,,b,,c")) == ["a", "b", "c"]
    assert list(parse_scopes("")) == []


def test_normalize_scopes():
    assert normalize_scopes("a,b,c") == "a,b,c"
    assert normalize_scopes("a, b, a, c") == "a,b,c"
    assert normalize_scopes(["a", " b ", "a", "c"]) == "a,b,c"
    assert normalize_scopes("") == ""
    assert normalize_scopes([]) == ""


def test_list_scopes():
    assert list_scopes("a,b,c") == ["a", "b", "c"]
    assert list_scopes("a, b, c") == ["a", "b", "c"]
