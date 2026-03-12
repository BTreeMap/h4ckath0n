"""Local filesystem storage backend."""

from __future__ import annotations

import hashlib
import os

from h4ckath0n.rng import token_hex as _rng_hex


async def store_file(storage_dir: str, data: bytes) -> tuple[str, str]:
    """Store file data and return (storage_key, sha256_hex).

    The storage key is fully opaque – it never contains any user-supplied
    values such as original filenames.
    """
    sha256 = hashlib.sha256(data).hexdigest()
    prefix = sha256[:2]
    random_part = _rng_hex(16)  # 128-bit opaque path component.
    storage_key = f"{prefix}/{random_part}"

    full_path = os.path.join(storage_dir, prefix)
    os.makedirs(full_path, exist_ok=True)

    file_path = os.path.join(storage_dir, storage_key)
    with open(file_path, "wb") as f:
        f.write(data)

    return storage_key, sha256


def get_file_path(storage_dir: str, storage_key: str) -> str:
    """Return the full filesystem path for a storage key.

    The storage key must be a server-generated opaque value.  This
    function validates that the resolved path stays within
    ``storage_dir`` to prevent path-traversal attacks.
    """
    safe_key = os.path.normpath(storage_key)
    if safe_key.startswith("..") or os.path.isabs(safe_key):
        raise ValueError("Invalid storage key")
    resolved = os.path.realpath(os.path.join(storage_dir, safe_key))
    base = os.path.realpath(storage_dir)
    if not resolved.startswith(base + os.sep) and resolved != base:
        raise ValueError("Invalid storage key")
    return resolved
