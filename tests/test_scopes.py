from h4ckath0n.auth.scopes import format_scopes, iter_scopes, parse_scopes


def test_iter_scopes() -> None:
    assert list(iter_scopes("a, b, , c ")) == ["a", "b", "c"]
    assert list(iter_scopes("")) == []


def test_parse_scopes() -> None:
    assert parse_scopes("a, b, , c, a ") == ["a", "b", "c"]


def test_format_scopes() -> None:
    assert format_scopes(["a ", "", "b", "a"]) == "a,b"
