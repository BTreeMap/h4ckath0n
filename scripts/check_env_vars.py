#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in Settings is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py

The script imports the h4ckath0n config Settings, enumerates all fields,
and checks that README.md mentions each corresponding environment variable.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[str]:
    """Return a list of environment variables defined by Settings."""
    from h4ckath0n.config import Settings  # noqa: E402

    env_vars: list[str] = []
    # Use Settings.model_fields directly to comply with SIM118
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            # Special case for OpenAI key where we support both
            env_vars.append("OPENAI_API_KEY")
            env_vars.append("H4CKATH0N_OPENAI_API_KEY")
        else:
            env_vars.append(f"H4CKATH0N_{field_name.upper()}")

    return env_vars


def check_vars_in_readme(env_vars: list[str]) -> list[str]:
    """Return environment variables that are not mentioned in README.md."""
    readme_text = README.read_text()
    missing: list[str] = []
    for var in env_vars:
        # Require the environment variable to be documented in backticks
        if f"`{var}`" not in readme_text:
            missing.append(var)
    return missing


def main() -> int:
    env_vars = get_env_vars()
    missing = check_vars_in_readme(env_vars)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these environment variables to README.md to ensure parity.")
        return 1

    print(f"✅ All {len(env_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
