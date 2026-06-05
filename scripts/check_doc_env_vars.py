#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in Settings is documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
sys.path.insert(0, str(REPO_ROOT / "src"))

from h4ckath0n.config import Settings  # noqa: E402


def check_env_vars_in_readme() -> list[str]:
    """Return environment variables that are not mentioned in README.md."""
    vars_to_check = []
    prefix = Settings.model_config.get("env_prefix", "H4CKATH0N_")

    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            vars_to_check.append("OPENAI_API_KEY")
            vars_to_check.append(f"{prefix}OPENAI_API_KEY".upper())
        else:
            vars_to_check.append(f"{prefix}{field_name}".upper())

    readme_text = README.read_text()
    missing: list[str] = []

    for var in vars_to_check:
        combined = rf"`{re.escape(var)}`"
        if not re.search(combined, readme_text):
            missing.append(var)

    return missing


def main() -> int:
    missing = check_env_vars_in_readme()

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these environment variables to README.md.")
        return 1

    print("✅ All environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
