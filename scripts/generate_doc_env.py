#!/usr/bin/env -S uv run python
"""Drift-prevention generator: output markdown table of configuration env vars.

Usage (from repo root):
    uv run scripts/generate_doc_env.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


from pydantic.fields import FieldInfo


def format_default(field_info: FieldInfo) -> str:
    default = field_info.default
    if default == "":
        return "empty"
    elif isinstance(default, bool):
        return f"`{str(default).lower()}`"
    elif isinstance(default, list):
        return "`[]`"
    return f"`{default}`"


def get_description(field_name: str) -> str:
    descriptions = {
        "env": "`development` or `production`",
        "database_url": "SQLAlchemy connection string",
        "auto_upgrade": "Auto-run packaged DB migrations to head on startup",
        "rp_id": "WebAuthn relying party ID, required in production",
        "origin": "WebAuthn origin, required in production",
        "webauthn_ttl_seconds": "WebAuthn challenge TTL in seconds",
        "user_verification": "WebAuthn user verification requirement",
        "attestation": "WebAuthn attestation preference",
        "password_auth_enabled": "Enable password routes when the extra is installed",
        "password_reset_expire_minutes": "Password reset token expiry in minutes",
        "bootstrap_admin_emails": "JSON list of emails that become admin on password signup",
        "first_user_is_admin": "First password signup becomes admin",
        "openai_api_key": "OpenAI API key for the LLM wrapper",
        "redis_url": "Redis connection string (optional)",
        "jobs_inline_in_dev": "Run background jobs inline in development",
        "jobs_default_queue": "Default background job queue name",
        "storage_backend": "Storage backend (`local`)",
        "storage_dir": "Local directory for storage backend",
        "max_upload_bytes": "Maximum upload size in bytes",
        "app_base_url": "Base URL of the frontend application",
        "email_backend": "Email backend to use (`file`, `smtp`)",
        "email_from": "Default From address for emails",
        "email_outbox_dir": "Directory for the file email backend",
        "smtp_host": "SMTP server host",
        "smtp_port": "SMTP server port",
        "smtp_username": "SMTP server username",
        "smtp_password": "SMTP server password",
        "smtp_starttls": "Use STARTTLS for SMTP",
        "smtp_ssl": "Use SSL for SMTP",
        "demo_mode": "Enable demo mode",
    }
    return descriptions.get(field_name, "")


def main() -> int:
    # Add src to sys.path to allow importing h4ckath0n
    src_path = REPO_ROOT / "src"
    sys.path.insert(0, str(src_path))

    from h4ckath0n.config import Settings  # noqa: E402

    lines = [
        "<!-- BEGIN GENERATED ENV VARS -->",
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for field_name, field_info in Settings.model_fields.items():
        if field_name == "openai_api_key":
            lines.append(f"| `OPENAI_API_KEY` | empty | {get_description(field_name)} |")
            lines.append(
                f"| `H4CKATH0N_OPENAI_API_KEY` | empty | Alternate {get_description(field_name)} |"
            )
            continue

        env_var = f"H4CKATH0N_{field_name.upper()}"
        default_val = format_default(field_info)

        # Check if there are specific overrides
        if field_name == "rp_id":
            default_val = "`localhost` in development"
        elif field_name == "origin":
            default_val = "`http://localhost:8000` in development"

        desc = get_description(field_name)
        lines.append(f"| `{env_var}` | {default_val} | {desc} |")

    lines.append("<!-- END GENERATED ENV VARS -->")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
