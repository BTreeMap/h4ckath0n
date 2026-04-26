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
    env: str = pydantic.Field("development", description="`development` or `production`")

    # --- database ---
    database_url: str = pydantic.Field(
        "sqlite:///./h4ckath0n.db", description="SQLAlchemy connection string"
    )
    auto_upgrade: bool = pydantic.Field(
        False, description="Auto-run packaged DB migrations to head on startup"
    )

    # --- WebAuthn / Passkeys ---
    rp_id: str = pydantic.Field(
        "", description="WebAuthn relying party ID, required in production"
    )
    origin: str = pydantic.Field("", description="WebAuthn origin, required in production")
    webauthn_ttl_seconds: int = pydantic.Field(
        300, description="WebAuthn challenge TTL in seconds"
    )
    user_verification: str = pydantic.Field(
        "preferred", description="WebAuthn user verification requirement"
    )
    attestation: str = pydantic.Field("none", description="WebAuthn attestation preference")

    # --- password auth (optional extra) ---
    password_auth_enabled: bool = pydantic.Field(
        False, description="Enable password routes when the extra is installed"
    )
    password_reset_expire_minutes: int = pydantic.Field(
        30, description="Password reset token expiry in minutes"
    )

    # --- admin bootstrap ---
    bootstrap_admin_emails: list[str] = pydantic.Field(
        default_factory=list,
        description="JSON list of emails that become admin on password signup",
    )
    first_user_is_admin: bool = pydantic.Field(
        False, description="First password signup becomes admin"
    )

    # --- LLM ---
    openai_api_key: str = pydantic.Field(
        "", description="Alternate OpenAI API key for the LLM wrapper"
    )

    # --- Redis ---
    redis_url: str = pydantic.Field("", description="Redis connection URL")
    jobs_inline_in_dev: bool = pydantic.Field(
        True, description="Run jobs inline in development mode"
    )
    jobs_default_queue: str = pydantic.Field(
        "default", description="Default queue name for background jobs"
    )

    # --- Storage ---
    storage_backend: str = pydantic.Field(
        "local", description="Storage backend to use (e.g. local, s3)"
    )
    storage_dir: str = pydantic.Field(
        "./.h4ckath0n_storage", description="Directory path for local storage backend"
    )
    max_upload_bytes: int = pydantic.Field(
        50 * 1024 * 1024, description="Maximum allowed upload size in bytes"
    )

    # --- Email ---
    app_base_url: str = pydantic.Field(
        "http://localhost:5173", description="Base URL of the application for generating links"
    )
    email_backend: str = pydantic.Field("file", description="Email backend to use (file or smtp)")
    email_from: str = pydantic.Field(
        "noreply@localhost", description="Default from address for outgoing emails"
    )
    email_outbox_dir: str = pydantic.Field(
        "./.h4ckath0n_email_outbox", description="Directory for file-based email backend"
    )
    smtp_host: str = pydantic.Field("", description="SMTP server host")
    smtp_port: int = pydantic.Field(587, description="SMTP server port")
    smtp_username: str = pydantic.Field("", description="SMTP username")
    smtp_password: str = pydantic.Field("", description="SMTP password")
    smtp_starttls: bool = pydantic.Field(True, description="Use STARTTLS for SMTP connection")
    smtp_ssl: bool = pydantic.Field(False, description="Use SSL/TLS for SMTP connection")

    # --- Demo ---
    demo_mode: bool = pydantic.Field(False, description="Enable demo mode restrictions")

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
