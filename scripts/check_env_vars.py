#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable from Settings is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[str]:
    """Return a list of environment variable names expected by Settings."""
    from h4ckath0n.config import Settings

    env_vars = []
    for key in Settings.model_fields:
        if key == "openai_api_key":
            # The config explicitly documents both for this specific field
            env_vars.append("OPENAI_API_KEY")
            env_vars.append("H4CKATH0N_OPENAI_API_KEY")
        else:
            env_vars.append(f"H4CKATH0N_{key.upper()}")

    return env_vars


def check_env_vars_in_readme(env_vars: list[str]) -> list[str]:
    """Return environment variables that are not mentioned in README.md."""
    readme_text = README.read_text(encoding="utf-8")
    missing: list[str] = []

    for var in env_vars:
        # Strictly match the variable name enclosed in backticks
        pattern = rf"`{var}`"
        if not re.search(pattern, readme_text):
            missing.append(var)

    return missing


def main() -> int:
    env_vars = get_env_vars()
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
