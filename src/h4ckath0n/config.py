"""Environment-driven configuration using pydantic-settings."""

from __future__ import annotations

import warnings

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
    env: str = "development"

    # --- database ---
    database_url: str = "sqlite:///./h4ckath0n.db"
    auto_upgrade: bool = False

    # --- WebAuthn / Passkeys ---
    rp_id: str = ""
    origin: str = ""
    webauthn_ttl_seconds: int = 300
    user_verification: str = "preferred"
    attestation: str = "none"

    # --- password auth (optional extra) ---
    password_auth_enabled: bool = False
    password_reset_expire_minutes: int = 30

    # --- admin bootstrap ---
    bootstrap_admin_emails: list[str] = []
    first_user_is_admin: bool = False

    # --- LLM ---
    openai_api_key: str = ""

    # --- Redis ---
    redis_url: str = ""
    jobs_inline_in_dev: bool = True
    jobs_default_queue: str = "default"

    # --- Storage ---
    storage_backend: str = "local"
    storage_dir: str = "./.h4ckath0n_storage"
    max_upload_bytes: int = 50 * 1024 * 1024  # 50 MB

    # --- Email ---
    app_base_url: str = "http://localhost:5173"
    email_backend: str = "file"  # "file" or "smtp"
    email_from: str = "noreply@localhost"
    email_outbox_dir: str = "./.h4ckath0n_email_outbox"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_starttls: bool = True
    smtp_ssl: bool = False

    # --- Demo ---
    demo_mode: bool = False

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
