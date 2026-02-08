"""Environment-driven configuration using pydantic-settings."""

from __future__ import annotations

import secrets
import warnings

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration. All values can be overridden via env vars prefixed ``H4CKRTH0N_``."""

    model_config = SettingsConfigDict(
        env_prefix="H4CKRTH0N_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- environment ---
    env: str = "development"

    # --- database ---
    database_url: str = "sqlite:///./h4ckrth0n.db"

    # --- auth / JWT ---
    auth_signing_key: str = ""
    auth_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    password_reset_expire_minutes: int = 30

    # --- admin bootstrap ---
    bootstrap_admin_emails: list[str] = []
    first_user_is_admin: bool = False

    # --- LLM ---
    openai_api_key: str = ""

    def effective_signing_key(self) -> str:
        """Return signing key, generating an ephemeral one in dev mode."""
        if self.auth_signing_key:
            return self.auth_signing_key
        if self.env == "production":
            raise RuntimeError("H4CKRTH0N_AUTH_SIGNING_KEY must be set in production mode.")
        ephemeral = secrets.token_urlsafe(32)
        warnings.warn(
            "Using an ephemeral JWT signing key. Set H4CKRTH0N_AUTH_SIGNING_KEY for production.",
            UserWarning,
            stacklevel=2,
        )
        return ephemeral
