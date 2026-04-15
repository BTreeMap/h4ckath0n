#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every config setting is documented.

Usage (from repo root):
    uv run scripts/check_doc_env.py

The script imports the h4ckath0n config Settings, enumerates all fields, and checks that
README.md mentions each one.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_config_fields() -> list[str]:
    from h4ckath0n.config import Settings

    return list(Settings.model_fields.keys())


def check_env_vars_in_readme(fields: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing: list[str] = []
    for field in fields:
        env_var = f"H4CKATH0N_{field.upper()}"
        if field == "openai_api_key":
            if "OPENAI_API_KEY" not in readme_text:
                missing.append(env_var)
            continue
        if env_var not in readme_text:
            missing.append(env_var)
    return missing


def main() -> int:
    fields = get_config_fields()
    missing = check_env_vars_in_readme(fields)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  `{env_var}`")
        print("\nAdd these environment variables to the Configuration section in README.md.")
        return 1

    print(f"✅ All {len(fields)} config environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
