#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable config is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
CONFIG_FILE = REPO_ROOT / "src" / "h4ckath0n" / "config.py"


def get_config_vars() -> list[str]:
    # Modify sys.path dynamically and use no_qa to prevent Ruff errors
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from h4ckath0n.config import Settings  # noqa: E402

    vars_list = []
    # Avoid SIM118 per style memory
    for field in Settings.model_fields:
        if field == "openai_api_key":
            vars_list.append("OPENAI_API_KEY")
            vars_list.append("H4CKATH0N_OPENAI_API_KEY")
        else:
            vars_list.append(f"H4CKATH0N_{field.upper()}")
    return sorted(set(vars_list))


def check_vars_in_readme(vars_list: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing = []
    for var in vars_list:
        pattern = rf"`{var}`"
        if not re.search(pattern, readme_text):
            missing.append(var)
    return missing


def main() -> int:
    vars_list = get_config_vars()
    missing = check_vars_in_readme(vars_list)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(vars_list)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
