#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in Settings is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_vars() -> list[str]:

    # Ensure src is in the path to import h4ckath0n
    sys.path.insert(0, str(REPO_ROOT / "src"))  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    vars = []
    # Using dictionary iteration per memory style guidelines
    for field in Settings.model_fields:
        vars.append(f"H4CKATH0N_{field.upper()}")
    return sorted(vars)


def check_vars_in_readme(vars: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing = []
    for var in vars:
        if rf"`{var}`" not in readme_text:
            missing.append(var)
    return missing


def main() -> int:
    vars = get_settings_vars()
    missing = check_vars_in_readme(vars)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
