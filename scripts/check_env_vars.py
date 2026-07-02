#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every config variable in Settings is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_keys() -> list[str]:
    from h4ckath0n.config import Settings  # noqa: E402

    return list(Settings.model_fields.keys())


def check_env_vars_in_readme(keys: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing: list[str] = []
    for key in keys:
        if key == "openai_api_key":
            if not re.search(r"`OPENAI_API_KEY`", readme_text) and not re.search(
                r"`H4CKATH0N_OPENAI_API_KEY`", readme_text
            ):
                missing.append("OPENAI_API_KEY")
            continue

        env_var = f"H4CKATH0N_{key.upper()}"
        if not re.search(rf"`{env_var}`", readme_text):
            missing.append(env_var)
    return missing


def main() -> int:
    keys = get_settings_keys()
    missing = check_env_vars_in_readme(keys)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these environment variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(keys)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
