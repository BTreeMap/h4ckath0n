"""Unified CSPRNG for h4ckath0n — a drop-in superset of the ``secrets`` module.

All functions draw from a per-thread SHAKE-128 XOF stream seeded from
``os.urandom`` at startup.  The stream is domain-separated so call-sites
are independent, and fork safety is handled automatically.

Engine
------
* Process-wide master key: ``os.urandom(32)`` at import time (never from env).
* Per-thread XOF reader: ``SHAKE128(domain || master_key || tid || os.urandom(16))``.
* Fork safety: child clears its inherited XOF state via ``os.register_at_fork``;
  falls back to PID checking when the hook is unavailable.

Public API
----------
The helpers below mirror ``secrets.*`` but always delegate to the XOF stream.

===================  ===========  ===============================================
Helper               Default (B)  Rationale
===================  ===========  ===============================================
``random_bytes``     (required)   Raw bytes; the shared primitive.
``random_base32``    20           32-char base32 ID, matches the library ID scheme.
``token_hex``        32           256-bit; reset tokens, storage keys, secrets.
``token_urlsafe``    32           256-bit; URL-safe flow IDs and bearer tokens.
``token_nonce``      8            64-bit collision-avoidance (filenames, logs).
``randbelow``        (required)   Uniform integer in [0, n); no modulo bias.
``choice``           (required)   Uniform element from a non-empty sequence.
===================  ===========  ===============================================

Why 32 bytes (256 bits) for tokens?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
128 bits resists brute-force at current compute scales; 256 bits adds a
comfortable margin beyond post-quantum collision bounds and matches NIST
SP 800-63B guidance for high-assurance secrets.  The extra bytes are free
when drawn from a streaming XOF.

Why 8 bytes for nonces?
~~~~~~~~~~~~~~~~~~~~~~~
A nonce avoids *accidental* collisions only (e.g. two emails in the same
microsecond).  Birthday-bounding 2⁶⁴ values gives < 10⁻⁹ collision
probability across a billion outputs — more than enough for any realistic
file-naming workload.
"""

from __future__ import annotations

import base64
import contextlib
import os
import sys
import threading
import warnings
from collections.abc import Sequence
from typing import TypeVar

from cryptography.hazmat.primitives import hashes

# ---------------------------------------------------------------------------
# Engine internals
# ---------------------------------------------------------------------------

# Domain separation tag — never reuse this string for another purpose.
_DOMAIN = b"h4ckath0n:idgen:v1\x00"

# Generated once at import time from the OS CSPRNG; never configurable via env.
_MASTER_KEY = os.urandom(32)

_U64_MASK = (1 << 64) - 1


def _u64le(x: int) -> bytes:
    # threading.get_ident() and os.getpid() are non-negative in practice.
    # Mask defensively to avoid OverflowError for unusually large platform values.
    return (x & _U64_MASK).to_bytes(8, "little", signed=False)


class _ShakeXOFReader:
    __slots__ = ("_xof",)

    def __init__(self, tid: int) -> None:
        alg = hashes.SHAKE128(digest_size=sys.maxsize)
        xof = hashes.XOFHash(alg)

        # Bind stream to: domain || master_key || tid || os.urandom(16)
        xof.update(_DOMAIN)
        xof.update(_MASTER_KEY)
        xof.update(_u64le(tid))
        xof.update(os.urandom(16))  # Extra per-reader OS randomness.

        self._xof = xof

    def read(self, nbytes: int) -> bytes:
        if nbytes < 0:
            raise ValueError("nbytes must be >= 0")
        return self._xof.squeeze(nbytes)


class _TLS(threading.local):
    # Typed thread-local slots for mypy (avoids Any from getattr on threading.local).
    reader: _ShakeXOFReader | None
    pid: int | None

    def __init__(self) -> None:
        self.reader = None
        self.pid = None


_tls = _TLS()


def _clear_tls_after_fork_child() -> None:
    # After fork the child inherits the parent's XOF state.  Clearing forces a
    # rebuild and ensures the child's stream diverges immediately.
    with contextlib.suppress(Exception):
        _tls.reader = None
        _tls.pid = None


_FORK_HOOK_INSTALLED = False
try:
    os.register_at_fork(after_in_child=_clear_tls_after_fork_child)
    _FORK_HOOK_INSTALLED = True
except AttributeError:
    _FORK_HOOK_INSTALLED = False
except Exception:
    _FORK_HOOK_INSTALLED = False

if not _FORK_HOOK_INSTALLED and hasattr(os, "fork"):
    warnings.warn(
        "Fork-safety hook (os.register_at_fork) is unavailable. This module will fall back to "
        "PID checking to avoid reusing inherited XOF state after fork, which adds a small "
        "per-call overhead. If you later remove the PID fallback and still fork, ID collisions "
        "can occur because the child can inherit the parent's XOF stream state.",
        RuntimeWarning,
        stacklevel=2,
    )


def _thread_reader() -> _ShakeXOFReader:
    reader = _tls.reader
    if reader is not None:
        if _FORK_HOOK_INSTALLED:
            return reader
        # Fallback: detect fork by PID change.
        pid = os.getpid()
        if _tls.pid == pid:
            return reader

    tid = threading.get_ident()
    reader = _ShakeXOFReader(tid)
    _tls.reader = reader
    if not _FORK_HOOK_INSTALLED:
        _tls.pid = os.getpid()
    return reader


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

T = TypeVar("T")

__all__ = [
    "random_bytes",
    "random_base32",
    "token_hex",
    "token_urlsafe",
    "token_nonce",
    "randbelow",
    "choice",
]


def random_bytes(nbytes: int) -> bytes:
    """Return *nbytes* cryptographically random bytes from the XOF stream.

    This is the shared primitive used by all higher-level helpers.

    Parameters
    ----------
    nbytes:
        Number of bytes to return.  Must be a positive integer.
    """
    if nbytes <= 0:
        raise ValueError("nbytes must be > 0")
    return _thread_reader().read(nbytes)


def random_base32(nbytes: int = 20) -> str:
    """Return a lowercase base32 string (no padding) from *nbytes* random bytes.

    The default of 20 bytes produces a 32-character string matching the
    library's ID scheme.  *nbytes* must be a multiple of 5 to avoid ``=``
    padding characters in RFC 4648 base32 output.

    Parameters
    ----------
    nbytes:
        Number of random bytes to draw.  Must be a positive multiple of 5.
    """
    if nbytes % 5 != 0:
        raise ValueError("nbytes must be a multiple of 5 to avoid base32 padding")
    raw = random_bytes(nbytes)
    return base64.b32encode(raw).decode("ascii").lower()


def token_hex(nbytes: int = 32) -> str:
    """Return a random lowercase hex string from *nbytes* random bytes (2×nbytes chars).

    The default of 32 bytes yields a 64-character string with 256 bits of
    entropy — suitable for password-reset tokens, storage-key random parts,
    and other opaque secrets.

    Parameters
    ----------
    nbytes:
        Number of random bytes to draw.  Default is 32 (256 bits).
    """
    return random_bytes(nbytes).hex()


def token_urlsafe(nbytes: int = 32) -> str:
    """Return a random URL-safe base64 string from *nbytes* random bytes.

    The default of 32 bytes yields roughly 43 characters with 256 bits of
    entropy — suitable for WebAuthn flow IDs, session handles, and any
    URL-embeddable opaque bearer credential.

    Encoding uses standard base64url (RFC 4648 §5) without padding.

    Parameters
    ----------
    nbytes:
        Number of random bytes to draw.  Default is 32 (256 bits).
    """
    return base64.urlsafe_b64encode(random_bytes(nbytes)).rstrip(b"=").decode("ascii")


def token_nonce(nbytes: int = 8) -> str:
    """Return a random lowercase hex string for *collision-avoidance* nonces only.

    Intentionally smaller than :func:`token_hex` — this is **not** a security
    boundary.  8 bytes (64 bits) gives a birthday-collision probability of
    < 10⁻⁹ across one billion outputs, which is sufficient for filename or
    log-correlation uniqueness.

    Parameters
    ----------
    nbytes:
        Number of random bytes.  Default is 8; reduce only with a clear reason.
    """
    return random_bytes(nbytes).hex()


def randbelow(n: int) -> int:
    """Return a uniformly random integer in [0, n) with no modulo bias.

    Uses rejection sampling, equivalent to ``secrets.randbelow``.

    Parameters
    ----------
    n:
        Exclusive upper bound.  Must be a positive integer.

    Raises
    ------
    ValueError:
        If *n* is not a positive integer.
    """
    if n <= 0:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return 0
    bit_length = (n - 1).bit_length()
    byte_length = (bit_length + 7) // 8
    mask = (1 << bit_length) - 1
    while True:
        candidate = int.from_bytes(random_bytes(byte_length), "big") & mask
        if candidate < n:
            return candidate


def choice(seq: Sequence[T]) -> T:
    """Return a uniformly random element from *seq*.

    Equivalent to ``secrets.choice``.  *seq* must be non-empty and support
    ``len`` and integer indexing.

    Parameters
    ----------
    seq:
        A non-empty sequence to pick from.

    Raises
    ------
    IndexError:
        If *seq* is empty.
    """
    if not seq:
        raise IndexError("Cannot choose from an empty sequence")
    return seq[randbelow(len(seq))]
