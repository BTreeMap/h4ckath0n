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
CONFIG_FILE = REPO_ROOT / "src" / "h4ckath0n" / "config.py"


def get_env_vars() -> list[str]:
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from h4ckath0n.config import Settings

    # Prefix is H4CKATH0N_
    prefix = Settings.model_config.get("env_prefix", "")

    vars = []
    for field_name in Settings.model_fields:
        vars.append(f"{prefix}{field_name}".upper())
    return sorted(vars)


def check_vars_in_readme(vars: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing = []
    for var in vars:
        # Check if the environment variable is present in a table cell or just in the file
        if f"`{var}`" not in readme_text:
            missing.append(var)
    return missing


def main() -> int:
    vars = get_env_vars()
    missing = check_vars_in_readme(vars)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
