#!/usr/bin/env -S uv run python
"""Drift check: verify that all configuration variables are documented.

Usage (from repo root):
    uv run scripts/check_doc_config.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_config_vars() -> list[str]:
    from h4ckath0n.config import Settings

    vars_list = []
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            vars_list.append("OPENAI_API_KEY")
            vars_list.append("H4CKATH0N_OPENAI_API_KEY")
        else:
            vars_list.append(f"H4CKATH0N_{field_name.upper()}")
    return sorted(vars_list)


def check_vars_in_readme(vars_list: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing = []
    for var in vars_list:
        if f"`{var}`" not in readme_text:
            missing.append(var)
    return missing


def main() -> int:
    vars_list = get_config_vars()
    missing = check_vars_in_readme(vars_list)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration section in README.md.")
        return 1

    print(f"✅ All {len(vars_list)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
