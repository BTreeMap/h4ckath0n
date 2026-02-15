"""h4ckath0n - ship hackathon products fast, securely."""

from h4ckath0n.app import create_app
from h4ckath0n.config import Settings
from h4ckath0n.version import __version__

__all__ = ["create_app", "Settings", "__version__"]
