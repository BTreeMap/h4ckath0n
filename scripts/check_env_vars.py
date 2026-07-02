#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_config_fields() -> list[str]:
    from h4ckath0n.config import Settings

    fields = []
    for field in Settings.model_fields:
        fields.append(field)
    return fields


def check_env_vars_in_readme(fields: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing: list[str] = []
    for field in fields:
        var_name = f"H4CKATH0N_{field.upper()}"
        if var_name not in readme_text:
            missing.append(var_name)
    return missing


def main() -> int:
    fields = get_config_fields()
    missing = check_env_vars_in_readme(fields)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(fields)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
