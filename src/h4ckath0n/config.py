"""Environment-driven configuration using pydantic-settings."""

from __future__ import annotations

import warnings

from pydantic import Field
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
    env: str = Field("development", description="`development` or `production`")

    # --- database ---
    database_url: str = Field(
        "sqlite:///./h4ckath0n.db", description="SQLAlchemy connection string"
    )
    auto_upgrade: bool = Field(
        False, description="Auto-run packaged DB migrations to head on startup"
    )

    # --- WebAuthn / Passkeys ---
    rp_id: str = Field("", description="WebAuthn relying party ID, required in production")
    origin: str = Field("", description="WebAuthn origin, required in production")
    webauthn_ttl_seconds: int = Field(300, description="WebAuthn challenge TTL in seconds")
    user_verification: str = Field(
        "preferred", description="WebAuthn user verification requirement"
    )
    attestation: str = Field("none", description="WebAuthn attestation preference")

    # --- password auth (optional extra) ---
    password_auth_enabled: bool = Field(
        False, description="Enable password routes when the extra is installed"
    )
    password_reset_expire_minutes: int = Field(
        30, description="Password reset token expiry in minutes"
    )

    # --- admin bootstrap ---
    bootstrap_admin_emails: list[str] = Field(
        [], description="JSON list of emails that become admin on password signup"
    )
    first_user_is_admin: bool = Field(False, description="First password signup becomes admin")

    # --- LLM ---
    openai_api_key: str = Field("", description="OpenAI API key for the LLM wrapper")

    # --- Redis ---
    redis_url: str = Field("", description="Redis connection string")
    jobs_inline_in_dev: bool = Field(
        True, description="Run jobs inline in development instead of queueing"
    )
    jobs_default_queue: str = Field(
        "default", description="Default queue name for background jobs"
    )

    # --- Storage ---
    storage_backend: str = Field("local", description="Storage backend (`local` or `s3`)")
    storage_dir: str = Field(
        "./.h4ckath0n_storage", description="Directory for local storage backend"
    )
    max_upload_bytes: int = Field(50 * 1024 * 1024, description="Maximum upload size in bytes")

    # --- Email ---
    app_base_url: str = Field(
        "http://localhost:5173", description="Base URL of the frontend application"
    )
    email_backend: str = Field("file", description="Email backend (`file` or `smtp`)")
    email_from: str = Field("noreply@localhost", description="Default sender address")
    email_outbox_dir: str = Field(
        "./.h4ckath0n_email_outbox", description="Directory for file email backend"
    )
    smtp_host: str = Field("", description="SMTP server hostname")
    smtp_port: int = Field(587, description="SMTP server port")
    smtp_username: str = Field("", description="SMTP username")
    smtp_password: str = Field("", description="SMTP password")
    smtp_starttls: bool = Field(True, description="Use STARTTLS for SMTP")
    smtp_ssl: bool = Field(False, description="Use SSL/TLS for SMTP")

    # --- Demo ---
    demo_mode: bool = Field(False, description="Enable read-only demo mode features")

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
