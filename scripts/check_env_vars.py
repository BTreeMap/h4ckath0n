#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that env vars in Settings are documented in the README."""

import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_expected_env_vars() -> list[str]:
    """Return all environment variables defined in Settings."""
    vars = []
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            vars.extend(["OPENAI_API_KEY", "H4CKATH0N_OPENAI_API_KEY"])
        else:
            vars.append(f"H4CKATH0N_{field_name.upper()}")
    return sorted(vars)


def check_env_vars_in_readme(expected_vars: list[str]) -> list[str]:
    """Return env vars that are not mentioned in README.md wrapped in backticks."""
    readme_text = README.read_text()
    missing = []
    for var in expected_vars:
        if f"`{var}`" not in readme_text:
            missing.append(var)
    return missing


def main() -> int:
    expected_vars = get_expected_env_vars()
    missing = check_env_vars_in_readme(expected_vars)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(expected_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
