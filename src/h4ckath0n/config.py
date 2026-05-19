"""Environment-driven configuration using pydantic-settings."""

from __future__ import annotations

import warnings

import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration. All values can be overridden via env vars prefixed ``H4CKATH0N_``."""

    model_config = SettingsConfigDict(
        env_prefix="H4CKATH0N_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- environment ---
    env: str = pydantic.Field(default="development", description="`development` or `production`")

    # --- database ---
    database_url: str = pydantic.Field(
        default="sqlite:///./h4ckath0n.db", description="SQLAlchemy connection string"
    )
    auto_upgrade: bool = pydantic.Field(
        default=False, description="Auto-run packaged DB migrations to head on startup"
    )

    # --- WebAuthn / Passkeys ---
    rp_id: str = pydantic.Field(
        default="", description="WebAuthn relying party ID, required in production"
    )
    origin: str = pydantic.Field(default="", description="WebAuthn origin, required in production")
    webauthn_ttl_seconds: int = pydantic.Field(
        default=300, description="WebAuthn challenge TTL in seconds"
    )
    user_verification: str = pydantic.Field(
        default="preferred", description="WebAuthn user verification requirement"
    )
    attestation: str = pydantic.Field(
        default="none", description="WebAuthn attestation preference"
    )

    # --- password auth (optional extra) ---
    password_auth_enabled: bool = pydantic.Field(
        default=False, description="Enable password routes when the extra is installed"
    )
    password_reset_expire_minutes: int = pydantic.Field(
        default=30, description="Password reset token expiry in minutes"
    )

    # --- admin bootstrap ---
    bootstrap_admin_emails: list[str] = pydantic.Field(
        default=[], description="JSON list of emails that become admin on password signup"
    )
    first_user_is_admin: bool = pydantic.Field(
        default=False, description="First password signup becomes admin"
    )

    # --- LLM ---
    openai_api_key: str = pydantic.Field(
        default="", description="OpenAI API key for the LLM wrapper"
    )

    # --- Redis ---
    redis_url: str = pydantic.Field(
        default="", description="Redis connection URL for background jobs"
    )
    jobs_inline_in_dev: bool = pydantic.Field(
        default=True, description="Run background jobs inline during development"
    )
    jobs_default_queue: str = pydantic.Field(
        default="default", description="Default queue name for background jobs"
    )

    # --- Storage ---
    storage_backend: str = pydantic.Field(
        default="local", description="Storage backend type (local, s3, etc)"
    )
    storage_dir: str = pydantic.Field(
        default="./.h4ckath0n_storage", description="Local directory for file storage"
    )
    max_upload_bytes: int = pydantic.Field(
        default=50 * 1024 * 1024, description="Maximum allowed upload size in bytes"
    )  # 50 MB

    # --- Email ---
    app_base_url: str = pydantic.Field(
        default="http://localhost:5173", description="Base URL for the frontend application"
    )
    email_backend: str = pydantic.Field(
        default="file", description="Email backend to use (file or smtp)"
    )
    email_from: str = pydantic.Field(
        default="noreply@localhost", description="Default sender address for emails"
    )
    email_outbox_dir: str = pydantic.Field(
        default="./.h4ckath0n_email_outbox",
        description="Directory to store emails when using file backend",
    )
    smtp_host: str = pydantic.Field(default="", description="SMTP server hostname")
    smtp_port: int = pydantic.Field(default=587, description="SMTP server port")
    smtp_username: str = pydantic.Field(default="", description="SMTP authentication username")
    smtp_password: str = pydantic.Field(default="", description="SMTP authentication password")
    smtp_starttls: bool = pydantic.Field(
        default=True, description="Use STARTTLS for SMTP connection"
    )
    smtp_ssl: bool = pydantic.Field(default=False, description="Use SSL/TLS for SMTP connection")

    # --- Demo ---
    demo_mode: bool = pydantic.Field(
        default=False, description="Enable demo mode with read-only restrictions"
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
