"""Local filesystem storage backend."""

from __future__ import annotations

import hashlib
import os
import secrets


async def store_file(storage_dir: str, data: bytes, original_filename: str) -> tuple[str, str]:
    """Store file data and return (storage_key, sha256_hex)."""
    sha256 = hashlib.sha256(data).hexdigest()
    # Create a safe storage key: sha256_prefix/random_hex_originalname
    prefix = sha256[:2]
    random_part = secrets.token_hex(8)
    safe_name = os.path.basename(os.path.normpath(original_filename))[:100]
    # Remove any remaining path separators or special characters
    safe_name = safe_name.replace(os.sep, "_").replace("/", "_").replace("\x00", "_")
    storage_key = f"{prefix}/{random_part}_{safe_name}"

    full_path = os.path.join(storage_dir, prefix)
    os.makedirs(full_path, exist_ok=True)

    file_path = os.path.join(storage_dir, storage_key)
    with open(file_path, "wb") as f:
        f.write(data)

    return storage_key, sha256


def get_file_path(storage_dir: str, storage_key: str) -> str:
    """Return the full filesystem path for a storage key."""
    # Ensure the key doesn't escape the storage directory
    safe_key = os.path.normpath(storage_key)
    if safe_key.startswith("..") or os.path.isabs(safe_key):
        raise ValueError("Invalid storage key")
    return os.path.join(storage_dir, safe_key)
