"""Prefixed base32 ID generators and validators.

Scheme
------
* Draw random bytes from the shared CSPRNG (``h4ckath0n.rng``).
* Base32-encode (lowercase, no padding) to produce a 32-character string.
* Replace the first character with a type prefix:

  - ``u`` for user IDs
  - ``k`` for internal credential (key) IDs
  - ``d`` for device IDs

* Password-reset tokens use 128-bit random hex (``new_token_id``).

All randomness comes from :mod:`h4ckath0n.rng`; this module contains only
the ID-scheme logic.
"""

from __future__ import annotations

from h4ckath0n.rng import random_base32, random_bytes

__all__ = [
    "new_user_id",
    "new_key_id",
    "new_device_id",
    "new_token_id",
    "is_user_id",
    "is_key_id",
    "is_device_id",
    # Re-export primitives for callers that imported them from here historically.
    "random_bytes",
    "random_base32",
]

_ID_LEN = 32
_ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyz234567")


def _new_prefixed_id(prefix: str) -> str:
    s = random_base32()
    return prefix + s[1:]


def _is_valid_prefixed_id(value: str, prefix: str) -> bool:
    return (
        len(value) == _ID_LEN
        and value[:1] == prefix
        and all(c in _ALLOWED_CHARS for c in value[1:])
    )


def new_user_id() -> str:
    """Generate a user ID (32 chars, starts with ``u``)."""
    return _new_prefixed_id("u")


def new_key_id() -> str:
    """Generate a credential key ID (32 chars, starts with ``k``)."""
    return _new_prefixed_id("k")


def new_device_id() -> str:
    """Generate a device ID (32 chars, starts with ``d``)."""
    return _new_prefixed_id("d")


def new_token_id() -> str:
    """Generate a generic token/row ID (128-bit random hex, 32 chars)."""
    return random_bytes(16).hex()


def is_user_id(value: str) -> bool:
    """Return ``True`` when *value* looks like a valid user ID."""
    return _is_valid_prefixed_id(value, "u")


def is_key_id(value: str) -> bool:
    """Return ``True`` when *value* looks like a valid key ID."""
    return _is_valid_prefixed_id(value, "k")


def is_device_id(value: str) -> bool:
    """Return ``True`` when *value* looks like a valid device ID."""
    return _is_valid_prefixed_id(value, "d")
