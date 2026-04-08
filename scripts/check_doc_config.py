#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all configuration settings in Settings are documented.

Usage (from repo root):
    uv run scripts/check_doc_config.py

The script imports the Settings model, enumerates all fields, and checks that
README.md mentions each one.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_fields() -> list[str]:
    """Return a list of environment variable names expected by the Settings model."""
    from h4ckath0n.config import Settings

    fields = []
    # pydantic_settings handles env_prefix
    prefix = Settings.model_config.get("env_prefix", "")
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            # Both without prefix and with prefix exist in README
            fields.append("OPENAI_API_KEY")
            fields.append(f"{prefix}OPENAI_API_KEY".upper())
            continue
        env_var = f"{prefix}{field_name}".upper()
        fields.append(env_var)
    return fields


def check_fields_in_readme(fields: list[str]) -> list[str]:
    """Return fields that are not mentioned in the README.md."""
    readme_text = README.read_text()
    missing: list[str] = []

    for field in fields:
        # Check if the exact env var name exists in the README surrounded by backticks
        pattern = rf"`{field}`"
        if not re.search(pattern, readme_text):
            missing.append(field)

    return missing


def main() -> int:
    fields = get_settings_fields()
    # deduplicate fields
    fields = list(set(fields))
    missing = check_fields_in_readme(fields)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for field in missing:
            print(f"  {field}")
        print("\nAdd these environment variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(fields)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
