"""Environment-driven configuration using pydantic-settings."""

from __future__ import annotations

import warnings
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

UserVerification = Literal["required", "preferred", "discouraged"]
AttestationConveyance = Literal["none", "indirect", "direct", "enterprise"]
EmailBackend = Literal["file", "smtp"]
StorageBackend = Literal["local"]


class Settings(BaseSettings):
    """Central configuration. All values can be overridden via env vars prefixed ``H4CKATH0N_``."""

    model_config = SettingsConfigDict(
        env_prefix="H4CKATH0N_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- environment ---
    env: str = Field(default="development", description="`development` or `production`")

    # --- database ---
    database_url: str = Field(
        default="sqlite:///./h4ckath0n.db", description="SQLAlchemy connection string"
    )
    auto_upgrade: bool = Field(
        default=False, description="Auto-run packaged DB migrations to head on startup"
    )

    # --- WebAuthn / Passkeys ---
    rp_id: str = Field(default="", description="WebAuthn relying party ID, required in production")
    origin: str = Field(default="", description="WebAuthn origin, required in production")
    webauthn_ttl_seconds: int = Field(default=300, description="WebAuthn challenge TTL in seconds")
    user_verification: UserVerification = Field(
        default="preferred", description="WebAuthn user verification requirement"
    )
    attestation: AttestationConveyance = Field(
        default="none", description="WebAuthn attestation preference"
    )

    # --- password auth (optional extra) ---
    password_auth_enabled: bool = Field(
        default=False, description="Enable password routes when the extra is installed"
    )
    password_reset_expire_minutes: int = Field(
        default=30, description="Password reset token expiry in minutes"
    )

    # --- admin bootstrap ---
    bootstrap_admin_emails: list[str] = Field(
        default_factory=list,
        description="JSON list of emails that become admin on password signup",
    )
    first_user_is_admin: bool = Field(
        default=False, description="First password signup becomes admin"
    )

    # --- LLM ---
    openai_api_key: str = Field(default="", description="OpenAI API key for the LLM wrapper")

    # --- Redis ---
    redis_url: str = Field(
        default="", description="Redis connection URL (e.g. redis://localhost:6379/0)"
    )
    jobs_inline_in_dev: bool = Field(
        default=True, description="Run jobs inline in development without a worker process"
    )
    jobs_default_queue: str = Field(
        default="default", description="Default queue name for background jobs"
    )

    # --- Storage ---
    storage_backend: StorageBackend = Field(
        default="local", description="Backend for file uploads (e.g. `local`)"
    )
    storage_dir: str = Field(
        default="./.h4ckath0n_storage", description="Directory for local file uploads"
    )
    max_upload_bytes: int = Field(
        default=50 * 1024 * 1024,
        description="Maximum allowed file upload size in bytes (default 50MB)",
    )

    # --- Email ---
    app_base_url: str = Field(
        default="http://localhost:5173",
        description="Base URL of the frontend application for email links",
    )
    email_backend: EmailBackend = Field(
        default="file", description="Email backend to use (`file` or `smtp`)"
    )
    email_from: str = Field(
        default="noreply@localhost", description="Default sender address for outbound emails"
    )
    email_outbox_dir: str = Field(
        default="./.h4ckath0n_email_outbox",
        description="Directory to store emails when using the `file` backend",
    )
    smtp_host: str = Field(default="", description="SMTP server hostname")
    smtp_port: int = Field(default=587, description="SMTP server port")
    smtp_username: str = Field(default="", description="SMTP authentication username")
    smtp_password: str = Field(default="", description="SMTP authentication password")
    smtp_starttls: bool = Field(default=True, description="Use STARTTLS for SMTP connections")
    smtp_ssl: bool = Field(default=False, description="Use explicit SSL/TLS for SMTP connections")

    # --- Demo ---
    demo_mode: bool = Field(
        default=False,
        description="Enable demo mode (e.g. injects fake latency, disables destructive actions)",
    )

    def effective_rp_id(self) -> str:
        """Return the WebAuthn relying party ID."""
        if self.rp_id:
            return self.rp_id
        if self.env == "production":
            raise RuntimeError("H4CKATH0N_RP_ID must be set in production mode.")
        warnings.warn(
            "Using 'localhost' as WebAuthn RP ID. Set H4CKATH0N_RP_ID for production.",
            UserWarning,
            stacklevel=2,
        )
        return "localhost"

    def effective_origin(self) -> str:
        """Return the expected WebAuthn origin."""
        if self.origin:
            return self.origin
        if self.env == "production":
            raise RuntimeError("H4CKATH0N_ORIGIN must be set in production mode.")
        warnings.warn(
            "Using 'http://localhost:8000' as WebAuthn origin. "
            "Set H4CKATH0N_ORIGIN for production.",
            UserWarning,
            stacklevel=2,
        )
        return "http://localhost:8000"
