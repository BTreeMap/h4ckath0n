#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var from Settings is documented in README.md.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_expected_env_vars() -> list[str]:
    """Return all expected env vars from Settings."""
    from h4ckath0n.config import Settings  # noqa: E402

    expected = []
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            expected.extend(["`OPENAI_API_KEY`", "`H4CKATH0N_OPENAI_API_KEY`"])
        else:
            expected.append(f"`H4CKATH0N_{field_name.upper()}`")
    return sorted(expected)


def check_env_vars_in_readme(expected_vars: list[str]) -> list[str]:
    """Return env vars that are missing from README.md."""
    readme_text = README.read_text()
    missing: list[str] = []

    for expected in expected_vars:
        if expected not in readme_text:
            missing.append(expected)

    return missing


def main() -> int:
    expected_vars = get_expected_env_vars()
    missing = check_env_vars_in_readme(expected_vars)

    if missing:
        print("❌ The following env vars from Settings are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these environment variables to the Configuration section in README.md.")
        return 1

    print(f"✅ All {len(expected_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
