#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[str]:
    from h4ckath0n.config import Settings

    vars_list = []
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            vars_list.append("OPENAI_API_KEY")
            vars_list.append("H4CKATH0N_OPENAI_API_KEY")
        else:
            vars_list.append(f"H4CKATH0N_{field_name.upper()}")

    return vars_list


def main() -> int:
    env_vars = get_env_vars()
    readme_text = README.read_text()

    missing = []
    for var in env_vars:
        if f"`{var}`" not in readme_text:
            missing.append(var)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        return 1

    print(f"✅ All {len(env_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
