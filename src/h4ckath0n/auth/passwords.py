"""Argon2id password hashing."""

from __future__ import annotations

from typing import cast

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_ph = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash *password* with Argon2id."""
    return cast(str, _ph.hash(password))


def verify_password(password: str, hash_: str) -> bool:
    """Verify *password* against an Argon2id *hash_*."""
    try:
        return cast(bool, _ph.verify(hash_, password))
    except VerifyMismatchError:
        return False


# Dummy hash generated with default Argon2id parameters (m=65536, t=3, p=4)
# Used to mitigate user enumeration timing attacks.
_DUMMY_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$GImMvPYDvWMIEDAytiwSBA"
    "$p1FXwJ1uVgRRc1+uda4vuysBwE2kQmx6hc880s661kY"
)


def verify_dummy_password(password: str) -> bool:
    """Perform a dummy verification to mitigate timing attacks."""
    return verify_password(password, _DUMMY_HASH)
