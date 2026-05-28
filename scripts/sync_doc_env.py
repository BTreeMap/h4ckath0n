#!/usr/bin/env -S uv run python
"""Drift-prevention generator: updates README.md Configuration."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- ENV_DOCS_START -->"
END_MARKER = "<!-- ENV_DOCS_END -->"


def format_default(field_info) -> str:
    """Format a default value for markdown."""
    from pydantic_core import PydanticUndefined

    default = field_info.default

    if default is PydanticUndefined:
        return "*required*"
    if default == "":
        return "empty"
    if isinstance(default, list):
        if not default:
            return "`[]`"
        return f"`{default}`"
    if isinstance(default, bool):
        return f"`{'true' if default else 'false'}`"
    if isinstance(default, (int, str)):
        return f"`{default}`"
    return f"`{default}`"


def generate_env_table() -> str:
    """Generate the markdown table for environment variables."""
    from h4ckath0n.config import Settings

    config_source = (REPO_ROOT / "src/h4ckath0n/config.py").read_text()

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        default_str = format_default(field_info)

        desc = ""
        for line in config_source.splitlines():
            # handle cases where the line might have spaces before the colon
            if re.match(rf"^\s*{name}\s*:", line):
                if "#" in line:
                    desc = line.split("#", 1)[1].strip()
                break

        # Handle special cases based on existing README
        var_name = f"`{var_name}`"

        if name == "rp_id":
            default_str = "`localhost` in development"
            desc = "WebAuthn relying party ID, required in production"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"
            desc = "WebAuthn origin, required in production"
        elif name == "database_url":
            desc = "SQLAlchemy connection string"
        elif name == "auto_upgrade":
            desc = "Auto-run packaged DB migrations to head on startup"
        elif name == "env":
            desc = "`development` or `production`"
        elif name == "webauthn_ttl_seconds":
            desc = "WebAuthn challenge TTL in seconds"
        elif name == "user_verification":
            desc = "WebAuthn user verification requirement"
        elif name == "attestation":
            desc = "WebAuthn attestation preference"
        elif name == "password_auth_enabled":
            desc = "Enable password routes when the extra is installed"
        elif name == "password_reset_expire_minutes":
            desc = "Password reset token expiry in minutes"
        elif name == "bootstrap_admin_emails":
            desc = "JSON list of emails that become admin on password signup"
        elif name == "first_user_is_admin":
            desc = "First password signup becomes admin"
        elif name == "openai_api_key":
            var_name = "`OPENAI_API_KEY` / `H4CKATH0N_OPENAI_API_KEY`"
            desc = "OpenAI API key for the LLM wrapper"
        else:
            pass

        lines.append(f"| {var_name} | {default_str} | {desc} |")

    return "\n".join(lines)


def sync_readme(dry_run: bool = False) -> int:
    """Sync the README file, or check if it's up to date in dry_run mode."""
    readme_text = README.read_text()

    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        print(f"❌ Error: {START_MARKER} or {END_MARKER} not found in README.md")
        return 1

    pattern = re.compile(rf"({START_MARKER}).*?({END_MARKER})", re.DOTALL)

    new_table = f"{START_MARKER}\n{generate_env_table()}\n{END_MARKER}"
    new_text = pattern.sub(new_table, readme_text)

    if dry_run:
        if readme_text != new_text:
            print("❌ README.md is out of date. Run `scripts/sync_doc_env.py` to update it.")
            return 1
        print("✅ README.md is up to date.")
        return 0

    if readme_text == new_text:
        print("✅ README.md is already up to date.")
        return 0

    README.write_text(new_text)
    print("✅ Updated README.md successfully.")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if README is up to date")
    args = parser.parse_args()

    sys.exit(sync_readme(dry_run=args.check))
