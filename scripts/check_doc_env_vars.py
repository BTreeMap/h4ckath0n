#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[str]:
    from h4ckath0n.config import Settings

    fields = Settings.model_fields
    vars = []
    for field_name in fields:
        if field_name == "openai_api_key":
            vars.append("OPENAI_API_KEY")
            vars.append("H4CKATH0N_OPENAI_API_KEY")
        else:
            vars.append(f"H4CKATH0N_{field_name.upper()}")
    return sorted(list(set(vars)))


def check_env_vars_in_readme(vars: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing: list[str] = []
    for var in vars:
        # Looking for `VAR_NAME`
        if f"`{var}`" not in readme_text:
            missing.append(var)
    return missing


def main() -> int:
    vars = get_env_vars()
    missing = check_env_vars_in_readme(vars)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these environment variables to README.md.")
        return 1

    print(f"✅ All {len(vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
