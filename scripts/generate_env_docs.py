#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that env vars in config.py match the README.md table."""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"

DESCRIPTIONS = {
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
    "openai_api_key": "Alternate OpenAI API key for the LLM wrapper",
    "redis_url": "Redis connection string (optional)",
    "jobs_inline_in_dev": "Run background jobs inline in development",
    "jobs_default_queue": "Default background job queue name",
    "storage_backend": "Storage backend type (e.g. `local`)",
    "storage_dir": "Directory for local storage",
    "max_upload_bytes": "Maximum upload size in bytes",
    "app_base_url": "Base URL of the web application",
    "email_backend": "Email backend (`file` or `smtp`)",
    "email_from": "Default from address for emails",
    "email_outbox_dir": "Directory for file-based email outbox",
    "smtp_host": "SMTP server host",
    "smtp_port": "SMTP server port",
    "smtp_username": "SMTP server username",
    "smtp_password": "SMTP server password",
    "smtp_starttls": "Enable STARTTLS for SMTP",
    "smtp_ssl": "Enable SSL for SMTP",
    "demo_mode": "Enable demo mode",
}


def generate_table() -> str:
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from h4ckath0n.config import Settings

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        default = "empty" if field.default == "" else f"`{field.default}`"
        default = default.replace("False", "false").replace("True", "true")
        if name == "rp_id":
            default = "`localhost` in development"
        if name == "origin":
            default = "`http://localhost:8000` in development"
        description = field.description or DESCRIPTIONS.get(name, "")
        lines.append(f"| `{var_name}` | {default} | {description} |")

    lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")

    return "\n".join(lines)


def update_readme(check: bool = False) -> int:
    readme_text = README.read_text()

    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        print(f"❌ Could not find {START_MARKER} and {END_MARKER} in README.md")
        return 1

    start_idx = readme_text.find(START_MARKER) + len(START_MARKER)
    end_idx = readme_text.find(END_MARKER)

    table = generate_table()
    new_readme = readme_text[:start_idx] + "\n\n" + table + "\n\n" + readme_text[end_idx:]

    if check:
        if readme_text != new_readme:
            print(
                "❌ README.md environment variables table is out of date. "
                "Run `uv run scripts/generate_env_docs.py` to update it."
            )
            return 1
        print("✅ README.md environment variables table is up to date.")
        return 0
    else:
        README.write_text(new_readme)
        print("✅ README.md environment variables table updated.")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="Check if the README.md table is up to date"
    )
    args = parser.parse_args()
    sys.exit(update_readme(args.check))
