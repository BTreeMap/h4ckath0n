from h4ckath0n.auth.scopes import format_scopes, parse_scopes


def test_parse_scopes_empty():
    assert parse_scopes("") == []
    assert parse_scopes("   ") == []


def test_parse_scopes_deduplicates():
    assert parse_scopes("foo, bar, foo") == ["foo", "bar"]


def test_parse_scopes_trims():
    assert parse_scopes("  foo  ,  bar  ") == ["foo", "bar"]


def test_parse_scopes_empty_items():
    assert parse_scopes("foo,,bar, ,baz") == ["foo", "bar", "baz"]


def test_format_scopes_empty():
    assert format_scopes([]) == ""


def test_format_scopes_trims_and_dedupes():
    assert format_scopes([" foo ", "bar", "foo", ""]) == "foo,bar"
