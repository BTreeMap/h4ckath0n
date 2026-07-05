#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var in Settings is documented in README.md.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[str]:
    from h4ckath0n.config import Settings

    vars_list = []
    for key in Settings.model_fields:
        vars_list.append(f"H4CKATH0N_{key.upper()}")
    return sorted(vars_list)


def check_vars_in_readme(env_vars: list[str]) -> list[str]:
    readme_text = README.read_text()

    match = re.search(r"(## Configuration\n\n.*?)(?=\n## )", readme_text, re.DOTALL)
    if not match:
        print("❌ Could not find '## Configuration' section in README.md")
        return env_vars

    config_section = match.group(1)

    missing = []
    for var in env_vars:
        # OPENAI_API_KEY is documented differently
        if var == "H4CKATH0N_OPENAI_API_KEY" and "H4CKATH0N_OPENAI_API_KEY" in config_section:
            continue

        if f"`{var}`" not in config_section:
            missing.append(var)
    return missing


def main() -> int:
    env_vars = get_env_vars()
    missing = check_vars_in_readme(env_vars)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(env_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
