#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all configuration settings in Settings are documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py

The script imports the h4ckath0n app Settings, extracts all setting fields, and checks that
README.md documents each one (prefixing them with H4CKATH0N_ or OPENAI_).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
SRC_PATH = REPO_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))


def get_settings_keys() -> list[str]:
    """Return all setting keys from Settings."""
    from h4ckath0n.config import Settings  # noqa: E402

    # Avoid SIM118 errors by iterating directly over the dictionary
    keys: list[str] = []
    for key in Settings.model_fields:
        keys.append(key)
    return sorted(keys)


def check_env_vars_in_readme(
    keys: list[str],
) -> list[str]:
    """Return env vars that are not documented in the configuration table."""
    readme_text = README.read_text()
    missing: list[str] = []

    # We look for ``H4CKATH0N_ENV`` etc in the markdown file
    for key in keys:
        env_var = key.upper() if key.startswith("openai_") else f"H4CKATH0N_{key.upper()}"

        # Build a pattern to find `ENV_VAR` in the markdown file
        combined = rf"`{re.escape(env_var)}`"
        if not re.search(combined, readme_text, re.IGNORECASE):
            missing.append(env_var)

    return missing


def main() -> int:
    keys = get_settings_keys()
    missing = check_env_vars_in_readme(keys)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  {env_var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(keys)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
