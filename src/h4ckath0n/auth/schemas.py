"""Pydantic schemas for auth endpoints."""

from __future__ import annotations

from collections.abc import Iterable

from pydantic import BaseModel, EmailStr, Field, field_validator

# Maximum length for display names (shared across DB, schemas, and API).
DISPLAY_NAME_MAX_LENGTH = 200


def _validate_display_name(v: str | None) -> str | None:
    """Trim whitespace; reject empty-after-trim values."""
    if v is None:
        return None
    v = v.strip()
    if v == "":
        return None
    return v


def parse_scopes(raw: str | Iterable[str] | None) -> list[str]:
    """Parse and deduplicate scopes from a string or iterable of strings."""
    if not raw:
        return []
    if isinstance(raw, str):
        raw = [raw]
    parts = (cleaned for item in raw for part in item.split(",") if (cleaned := part.strip()))
    return list(dict.fromkeys(parts))


def format_scopes(scopes: str | Iterable[str] | None) -> str:
    """Format scopes into a normalized comma-separated string."""
    return ",".join(parse_scopes(scopes))


class DeviceBindingMixin(BaseModel):
    device_public_key_jwk: dict | None = Field(
        None,
        description="Optional device public key in JWK format to bind a device identity.",
    )
    device_label: str | None = Field(None, description="Optional label for the device.")


class RegisterRequest(DeviceBindingMixin):
    email: EmailStr = Field(..., description="Account email for password-based signup.")
    password: str = Field(..., description="Plaintext password, hashed server-side.")
    display_name: str = Field(
        ...,
        description="Human-facing display name for the account.",
        max_length=DISPLAY_NAME_MAX_LENGTH,
    )

    @field_validator("display_name")
    @classmethod
    def _clean_display_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Display name must not be empty")
        return v


class LoginRequest(DeviceBindingMixin):
    email: EmailStr = Field(..., description="Account email for password-based login.")
    password: str = Field(..., description="Plaintext password to verify.")


class DeviceBindingResponse(BaseModel):
    user_id: str = Field(..., description="User ID that starts with the u prefix.")
    device_id: str = Field(
        ...,
        description="Device ID that starts with the d prefix, empty when no device key is bound.",
    )
    role: str = Field(..., description="Server-side role for the user.")
    display_name: str | None = Field(
        None,
        description="Human-facing display name for the user.",
    )


class PasswordResetRequestSchema(BaseModel):
    email: EmailStr = Field(..., description="Account email to send a reset token.")


class PasswordResetConfirmSchema(DeviceBindingMixin):
    token: str = Field(..., description="Password reset token issued by the server.")
    new_password: str = Field(..., description="New password to set for the account.")


class MessageResponse(BaseModel):
    message: str = Field(..., description="Human-readable response message.")


class SessionResponse(BaseModel):
    """Current authenticated session info."""

    user_id: str = Field(..., description="User ID.")
    device_id: str = Field(..., description="Device ID from the verified JWT.")
    role: str = Field(..., description="Server-side role.")
    scopes: list[str] = Field(..., description="User scopes as a list.")
    display_name: str | None = Field(None, description="Display name.")
    email: str | None = Field(None, description="User email if set.")


class ErrorResponse(BaseModel):
    """Standard error envelope for auth routes."""

    detail: str | dict[str, str] = Field(
        ...,
        description="Error detail message or structured error payload.",
    )
