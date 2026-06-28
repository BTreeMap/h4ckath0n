"""Argon2id password hashing."""

from __future__ import annotations

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_ph = PasswordHasher()

# 🛡️ Sentinel: A structurally valid Argon2id hash used to mitigate timing attacks.
DUMMY_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$6aYSXs+yKK819dL80MR3CQ$W1t5zfU3JQOaeh4"
    "zo6OJTY7PFUkf0/pkMQ8iwQk1s5M"
)


def hash_password(password: str) -> str:
    """Hash *password* with Argon2id."""
    return _ph.hash(password)


def verify_password(password: str, hash_: str) -> bool:
    """Verify *password* against an Argon2id *hash_*."""
    try:
        return _ph.verify(hash_, password)
    except VerifyMismatchError:
        return False
