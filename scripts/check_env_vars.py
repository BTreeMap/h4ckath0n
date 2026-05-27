#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in Settings is documented.

This script ensures that all fields defined in the Pydantic Settings model are explicitly
mentioned in the README.md file to prevent drift between the code and the documentation.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_fields() -> list[str]:
    from h4ckath0n.config import Settings

    fields = []
    for field in Settings.model_fields:
        fields.append(f"H4CKATH0N_{field.upper()}")
    if "OPENAI_API_KEY" not in fields:
        fields.append("OPENAI_API_KEY")
    return fields


def check_env_vars_in_readme(env_vars: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing = []
    for env_var in env_vars:
        if env_var == "H4CKATH0N_OPENAI_API_KEY":
            continue
        # We look for `VAR_NAME` or just VAR_NAME
        if f"`{env_var}`" not in readme_text and env_var not in readme_text:
            missing.append(env_var)
    return missing


def main() -> int:
    env_vars = get_settings_fields()
    missing = check_env_vars_in_readme(env_vars)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  {env_var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(env_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
