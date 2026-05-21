#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in Settings is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py

The script imports the Settings class, enumerates all fields, and checks that
README.md mentions each one in the Configuration table.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_env_vars() -> list[str]:
    """Return a list of environment variable names from Settings."""
    from h4ckath0n.config import Settings  # noqa: E402

    env_vars = []
    # Hardcoded or special environment variables
    env_vars.append("OPENAI_API_KEY")

    # Access model_fields on the class itself to avoid PydanticDeprecatedSince211
    for field_name in Settings.model_fields:
        env_vars.append(f"H4CKATH0N_{field_name.upper()}")

    return sorted(env_vars)


def check_env_vars_in_readme(env_vars: list[str]) -> list[str]:
    """Return env vars that are not mentioned in README.md."""
    readme_text = README.read_text()
    missing: list[str] = []
    for var in env_vars:
        # Check if var is in the markdown text (specifically as code block)
        pattern = rf"`{var}`"
        if not re.search(pattern, readme_text):
            missing.append(var)
    return missing


def main() -> int:
    env_vars = get_settings_env_vars()
    missing = check_env_vars_in_readme(env_vars)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(env_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
