#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the config table in README.md is up to date."""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_table() -> str:
    from h4ckath0n.config import Settings

    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in Settings.model_fields.items():
        if getattr(type(field.default), "__name__", "") == "PydanticUndefinedType":
            default_val = "empty"
        else:
            if name == "max_upload_bytes" and field.default == 50 * 1024 * 1024:
                default_val = "`50 * 1024 * 1024`"
            elif field.default == "":
                default_val = "empty"
            elif field.default == []:
                default_val = "`[]`"
            elif isinstance(field.default, bool):
                default_val = f"`{'true' if field.default else 'false'}`"
            else:
                default_val = f"`{field.default}`"

        env_name = f"`H4CKATH0N_{name.upper()}`"

        desc = field.description or ""

        if name == "env":
            desc = "`development` or `production`"
        if name == "database_url":
            desc = "SQLAlchemy connection string"
        if name == "auto_upgrade":
            desc = "Auto-run packaged DB migrations to head on startup"
        if name == "rp_id":
            default_val = "`localhost` in development"
            desc = "WebAuthn relying party ID, required in production"
        if name == "origin":
            default_val = "`http://localhost:8000` in development"
            desc = "WebAuthn origin, required in production"
        if name == "webauthn_ttl_seconds":
            desc = "WebAuthn challenge TTL in seconds"
        if name == "user_verification":
            desc = "WebAuthn user verification requirement"
        if name == "attestation":
            desc = "WebAuthn attestation preference"
        if name == "password_auth_enabled":
            desc = "Enable password routes when the extra is installed"
        if name == "password_reset_expire_minutes":
            desc = "Password reset token expiry in minutes"
        if name == "bootstrap_admin_emails":
            desc = "JSON list of emails that become admin on password signup"
        if name == "first_user_is_admin":
            desc = "First password signup becomes admin"
        if name == "openai_api_key":
            desc = "Alternate OpenAI API key for the LLM wrapper"
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
        if name == "redis_url":
            desc = "Redis connection string"
        if name == "jobs_inline_in_dev":
            desc = "Run jobs synchronously in development mode"
        if name == "jobs_default_queue":
            desc = "Default queue name for background jobs"
        if name == "storage_backend":
            desc = "`local` or `s3`"
        if name == "storage_dir":
            desc = "Directory for local storage backend"
        if name == "max_upload_bytes":
            desc = "Maximum upload size in bytes"
        if name == "app_base_url":
            desc = "Base URL for the frontend application, used in emails"
        if name == "email_backend":
            desc = "`file` or `smtp`"
        if name == "email_from":
            desc = "Default sender address for emails"
        if name == "email_outbox_dir":
            desc = "Directory for file email backend"
        if name == "smtp_host":
            desc = "SMTP server host"
        if name == "smtp_port":
            desc = "SMTP server port"
        if name == "smtp_username":
            desc = "SMTP username"
        if name == "smtp_password":
            desc = "SMTP password"
        if name == "smtp_starttls":
            desc = "Use STARTTLS for SMTP"
        if name == "smtp_ssl":
            desc = "Use SSL/TLS for SMTP"
        if name == "demo_mode":
            desc = "Enable demo mode features and restrictions"

        lines.append(f"| {env_name} | {default_val} | {desc} |")

    return "\n".join(lines)


def update_readme(check: bool = False) -> int:
    table = generate_table()
    content = README.read_text()

    start_marker = "<!-- CONFIG_TABLE_START -->"
    end_marker = "<!-- CONFIG_TABLE_END -->"

    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)

    new_table_block = f"{start_marker}\n{table}\n{end_marker}"

    if not re.search(pattern, content):
        print("❌ Could not find config table markers in README.md")
        return 1

    new_content = re.sub(pattern, new_table_block, content)

    if content == new_content:
        print("✅ Config table is up to date.")
        return 0

    if check:
        print("❌ Config table is out of date. Run `uv run scripts/generate_doc_config.py`.")
        return 1

    README.write_text(new_content)
    print("✅ Config table updated.")
    return 0


if __name__ == "__main__":
    check_mode = "--check" in sys.argv
    sys.exit(update_readme(check=check_mode))
