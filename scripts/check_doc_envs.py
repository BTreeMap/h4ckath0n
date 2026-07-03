#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every configuration setting in the app is documented.

Usage (from repo root):
    uv run scripts/check_doc_envs.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_config_vars() -> list[str]:
    """Return the expected environment variable names from Settings."""
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from h4ckath0n.config import Settings  # noqa: E402

    fields = Settings.model_fields
    vars_list = []
    for name in fields:
        env_name = f"H4CKATH0N_{name.upper()}"
        vars_list.append(env_name)
    return sorted(vars_list)


def check_envs_in_readme(vars_list: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing = []
    for var in vars_list:
        if f"`{var}`" not in readme_text:
            missing.append(var)
    return missing


def main() -> int:
    vars_list = get_config_vars()
    missing = check_envs_in_readme(vars_list)

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
