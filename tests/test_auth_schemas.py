from __future__ import annotations

import pytest

from h4ckath0n.auth.schemas import format_scopes, parse_scopes


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        # String inputs
        ("", []),
        ("   ", []),
        ("admin", ["admin"]),
        ("admin,user", ["admin", "user"]),
        ("  admin  ,  user  ", ["admin", "user"]),
        ("admin,,user,", ["admin", "user"]),
        ("admin,admin", ["admin"]),
        ("admin,user,admin", ["admin", "user"]),
        # Iterable inputs
        ([], []),
        ([""], []),
        (["   "], []),
        (["admin"], ["admin"]),
        (["admin", "user"], ["admin", "user"]),
        (["  admin  ", "  user  "], ["admin", "user"]),
        (["admin", "", "user", None], ["admin", "user"]),
        (["admin", "admin"], ["admin"]),
        (["admin", "user", "admin"], ["admin", "user"]),
        # Tuple
        (("admin", "user", "admin"), ["admin", "user"]),
    ],
)
def test_parse_scopes(raw: str | list[str] | tuple[str, ...], expected: list[str]) -> None:
    assert parse_scopes(raw) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("", ""),
        ("   ", ""),
        ("admin", "admin"),
        ("admin,user", "admin,user"),
        ("  admin  ,  user  ", "admin,user"),
        ("admin,,user,", "admin,user"),
        ("admin,admin", "admin"),
        ("admin,user,admin", "admin,user"),
        ([], ""),
        ([""], ""),
        (["   "], ""),
        (["admin"], "admin"),
        (["admin", "user"], "admin,user"),
        (["  admin  ", "  user  "], "admin,user"),
        (["admin", "admin"], "admin"),
        (["admin", "user", "admin"], "admin,user"),
    ],
)
def test_format_scopes(raw: str | list[str], expected: str) -> None:
    assert format_scopes(raw) == expected
