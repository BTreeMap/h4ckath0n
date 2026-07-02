#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable is documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[str]:
    # We must insert the src directory into sys.path to import local modules directly
    sys.path.insert(0, str(REPO_ROOT / "src"))  # noqa: E402
    from h4ckath0n.config import Settings
    from h4ckath0n.obs.settings import ObservabilitySettings

    env_vars = []

    # Settings has prefix H4CKATH0N_
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            env_vars.append("OPENAI_API_KEY")
            env_vars.append("H4CKATH0N_OPENAI_API_KEY")
        else:
            env_vars.append(f"H4CKATH0N_{field_name.upper()}")

    # ObservabilitySettings has no prefix
    for field_name in ObservabilitySettings.model_fields:
        env_vars.append(field_name.upper())

    return env_vars


def check_env_vars_in_readme(env_vars: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing = []
    for var in env_vars:
        # Check for strict match enclosed in backticks
        if f"`{var}`" not in readme_text:
            missing.append(var)
    return missing


def main() -> int:
    env_vars = get_env_vars()
    missing = check_env_vars_in_readme(env_vars)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration section in README.md.")
        return 1

    print(f"✅ All {len(env_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
