#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every configuration variable is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py

The script imports the Settings class from h4ckath0n.config, enumerates all fields,
and checks that README.md mentions each one in the Configuration table.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
SRC_PATH = REPO_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))
from h4ckath0n.config import Settings  # noqa: E402


def check_env_vars_in_readme() -> list[str]:
    """Return env vars that are not mentioned anywhere in README.md."""
    readme_text = README.read_text()
    missing: list[str] = []

    for field in Settings.model_fields:
        # Construct the expected environment variable name
        env_var = f"H4CKATH0N_{field.upper()}"

        # We look for the env var enclosed in backticks in the README
        pattern = rf"`{env_var}`"
        if not re.search(pattern, readme_text):
            missing.append(env_var)

    return missing


def main() -> int:
    missing = check_env_vars_in_readme()

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  {env_var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(
        f"✅ All {len(Settings.model_fields)} environment variables are documented in README.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
