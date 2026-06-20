"""Typed domain errors for the passkey (WebAuthn) subsystem.

Each error carries a stable, machine-readable ``code`` so HTTP and CLI layers
can map failures to responses without inspecting human-readable message text.

These errors subclass :class:`ValueError` so that the existing service
contract (``raise ValueError`` on invalid preconditions) is preserved for
callers that catch the broad type.
"""

from __future__ import annotations

from typing import ClassVar


class PasskeyError(ValueError):
    """Base class for passkey domain errors.

    Subclasses define a class-level :attr:`code` and a default message.
    """

    code: ClassVar[str] = "PASSKEY_ERROR"
    default_message: ClassVar[str] = "Passkey operation failed."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class PasskeyNotFoundError(PasskeyError):
    """The referenced credential does not exist or is not owned by the user."""

    code = "PASSKEY_NOT_FOUND"
    default_message = "Credential not found"


class PasskeyAlreadyRevokedError(PasskeyError):
    """The credential targeted for revocation is already revoked."""

    code = "PASSKEY_ALREADY_REVOKED"
    default_message = "Credential already revoked"


class PasskeyRevokedError(PasskeyError):
    """A revoked credential cannot be mutated (e.g. renamed)."""

    code = "PASSKEY_REVOKED"
    default_message = "Cannot rename a revoked passkey"


class LastPasskeyError(PasskeyError):
    """Revoking this credential would leave the user with no way to sign in."""

    code = "LAST_PASSKEY"
    default_message = (
        "Cannot revoke the last active passkey. "
        "Add another passkey via POST /auth/passkey/add/start first."
    )
