"""h4ckath0n - ship hackathon products fast, securely."""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

# Used only when running from source without installed package metadata.
__fallback_version__ = "0.1.1"

try:
    __version__ = _pkg_version("h4ckath0n")
except PackageNotFoundError:
    __version__ = __fallback_version__

from h4ckath0n.app import create_app
from h4ckath0n.config import Settings

__all__ = ["create_app", "Settings", "__version__"]
