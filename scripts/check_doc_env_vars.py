#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in Settings is documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py

The script imports the h4ckath0n app settings, enumerates all fields, and checks that
README.md mentions each one enclosed in backticks.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[str]:
    from h4ckath0n.config import Settings

    env_vars = []
    prefix = Settings.model_config.get("env_prefix", "")
    for field_name in Settings.model_fields:
        if field_name.lower() == "openai_api_key":
            env_vars.append("OPENAI_API_KEY")
            env_vars.append(f"{prefix.upper()}OPENAI_API_KEY")
        else:
            env_vars.append(f"{prefix.upper()}{field_name.upper()}")
    return list(set(env_vars))


def check_env_vars_in_readme(env_vars: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing: list[str] = []
    for var in env_vars:
        if f"`{var}`" not in readme_text:
            missing.append(var)
    return sorted(missing)


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
