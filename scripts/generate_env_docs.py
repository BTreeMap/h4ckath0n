#!/usr/bin/env -S uv run python
"""Drift-prevention script to generate env var docs from pydantic config.

Usage (from repo root):
    uv run scripts/generate_env_docs.py [--check]
"""

import argparse
import re
import sys
from pathlib import Path

# Add src to pythonpath so we can import h4ckath0n
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def get_env_vars_table() -> str:
    """Generate Markdown table for all fields in Settings."""
    rows = []
    rows.append("| Variable | Default | Description |")
    rows.append("|---|---|---|")

    # We map field names to descriptions manually, or extract from docstrings.
    # To keep it simple, we use a predefined dictionary of descriptions since pydantic
    # doesn't store descriptions directly unless we use Field(description=...)
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
        "redis_url": "Redis connection URL",
        "jobs_inline_in_dev": "Run jobs synchronously in development mode",
        "jobs_default_queue": "Default queue name for background jobs",
        "storage_backend": "Storage backend ('local' or 's3')",
        "storage_dir": "Local directory for uploaded files",
        "max_upload_bytes": "Maximum allowed upload size in bytes",
        "app_base_url": "Base URL of the web application",
        "email_backend": "Email backend ('file' or 'smtp')",
        "email_from": "Sender email address",
        "email_outbox_dir": "Local directory for file-based email outbox",
        "smtp_host": "SMTP server host",
        "smtp_port": "SMTP server port",
        "smtp_username": "SMTP authentication username",
        "smtp_password": "SMTP authentication password",
        "smtp_starttls": "Enable STARTTLS for SMTP",
        "smtp_ssl": "Enable SSL for SMTP",
        "demo_mode": "Enable demo mode features",
    }

    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            var_name = f"`OPENAI_API_KEY`<br>`H4CKATH0N_{name.upper()}`"
        else:
            var_name = f"`H4CKATH0N_{name.upper()}`"

        default = field.default
        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"
        elif default == "" or default == []:
            default_str = "empty"
        elif default is False:
            default_str = "`false`"
        elif default is True:
            default_str = "`true`"
        else:
            default_str = f"`{default}`"

        desc = descriptions.get(name, "")
        rows.append(f"| {var_name} | {default_str} | {desc} |")

    return "\n".join(rows)


def update_readme(check_only: bool = False) -> int:
    readme_text = README.read_text()
    table = get_env_vars_table()

    # Check if markers exist
    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        # We'll replace the existing manual table
        # Let's find the Configuration section
        print(
            "Markers not found, please manually add <!-- BEGIN ENV VARS --> and "
            "<!-- END ENV VARS --> around the table in README.md"
        )
        return 1

    pattern = re.compile(rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL)
    new_content = f"{START_MARKER}\n{table}\n{END_MARKER}"

    new_readme = pattern.sub(new_content, readme_text)

    if new_readme == readme_text:
        if check_only:
            print("✅ README.md env vars are up to date.")
        return 0

    if check_only:
        print("❌ README.md env vars are out of date.")
        print("Run `uv run scripts/generate_env_docs.py` to update.")
        return 1

    README.write_text(new_readme)
    print("✅ Updated README.md env vars.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check only, do not write")
    args = parser.parse_args()
    sys.exit(update_readme(args.check))
