from h4ckath0n.auth.scopes import format_scopes, parse_scopes


class TestScopesParsing:
    def test_basic(self):
        assert parse_scopes("a,b,c") == ["a", "b", "c"]
        assert format_scopes(["a", "b", "c"]) == "a,b,c"

    def test_dedup(self):
        assert parse_scopes("a,b,a") == ["a", "b"]
        assert format_scopes(["a", "b", "a"]) == "a,b"

    def test_trim(self):
        assert parse_scopes(" a , b , c ") == ["a", "b", "c"]
        assert format_scopes([" a ", " b ", " c "]) == "a,b,c"

    def test_empty_segments(self):
        assert parse_scopes("a,,b,,") == ["a", "b"]
        assert format_scopes(["a", "", "b", "", ""]) == "a,b"

    def test_empty_string(self):
        assert parse_scopes("") == []
        assert format_scopes([]) == ""

    def test_none_parsing(self):
        assert parse_scopes(None) == []
