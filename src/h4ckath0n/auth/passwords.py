"""Argon2id password hashing."""

from __future__ import annotations

from typing import cast

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError

_ph = PasswordHasher()

_DUMMY_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4"
    "$Bhzpsiy+FDoEr3tyJutf5g$lD1dAjeDNtYtN2cKj7+PkNLGpa1CURL/UThCNcioVaw"
)


def hash_password(password: str) -> str:
    """Hash *password* with Argon2id."""
    return cast(str, _ph.hash(password))


def verify_password(password: str, hash_: str) -> bool:
    """Verify *password* against an Argon2id *hash_*."""
    try:
        return cast(bool, _ph.verify(hash_, password))
    except (InvalidHashError, VerifyMismatchError):
        return False
