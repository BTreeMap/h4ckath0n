#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in Settings is documented.

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
    """Return environment variables from Settings."""
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from h4ckath0n.config import Settings  # noqa: E402

    prefix = Settings.model_config.get("env_prefix", "")
    env_vars: list[str] = []

    for field in Settings.model_fields:
        env_vars.append(f"{prefix}{field}".upper())

    if "OPENAI_API_KEY" not in env_vars:
        env_vars.append("OPENAI_API_KEY")

    return sorted(env_vars)


def check_env_vars_in_readme(env_vars: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing: list[str] = []
    for var in env_vars:
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
        print("\nAdd these to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(env_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
