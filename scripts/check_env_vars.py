#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that env vars in the Settings model are documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
SRC_PATH = REPO_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))


def get_config_env_vars() -> list[str]:
    from h4ckath0n.config import Settings  # noqa: E402

    env_vars: list[str] = []
    for field_name in Settings.model_fields:
        env_vars.append(f"H4CKATH0N_{field_name.upper()}")

    return env_vars


def check_env_vars_in_readme(env_vars: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing: list[str] = []
    for var in env_vars:
        if f"`{var}`" not in readme_text:
            missing.append(var)
    return missing


def main() -> int:
    env_vars = get_config_env_vars()
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
