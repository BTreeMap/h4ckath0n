"""Authorization domain types: roles and scopes.

Roles and scopes were previously passed around as bare strings and parsed
ad-hoc from comma-separated values at several call sites.  This module
centralises that logic so the CSV representation lives in exactly one place
and authorization values carry intent in the type system.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, NewType

# A user's privilege tier.  Stored as a short string in the database.
Role = Literal["user", "admin"]

USER: Role = "user"
ADMIN: Role = "admin"

# A single authorization scope (e.g. ``"admin"``, ``"demo"``).  Scopes are
# persisted as a comma-separated string for backwards compatibility.
Scope = NewType("Scope", str)


def parse_scopes(raw: str) -> list[Scope]:
    """Parse a comma-separated scope string into an ordered, de-duplicated list.

    Whitespace around each scope is trimmed and empty entries are dropped.
    Insertion order is preserved so serialisation round-trips stably.
    """
    cleaned = (part.strip() for part in raw.split(","))
    return [Scope(part) for part in dict.fromkeys(p for p in cleaned if p)]


def serialize_scopes(scopes: Iterable[Scope]) -> str:
    """Serialise scopes back into the canonical comma-separated form."""
    return ",".join(dict.fromkeys(str(s) for s in scopes if s))


def missing_scopes(granted: Iterable[Scope], required: Iterable[Scope]) -> set[Scope]:
    """Return the required scopes that are not present in *granted*."""
    return set(required).difference(granted)
