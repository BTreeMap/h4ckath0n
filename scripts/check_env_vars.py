#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every configuration setting in Settings is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_fields() -> list[str]:
    from h4ckath0n.config import Settings  # noqa: E402

    return list(Settings.model_fields)


def check_env_vars_in_readme(fields: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing: list[str] = []

    for field in fields:
        env_var_name = f"H4CKATH0N_{field.upper()}"
        if field == "openai_api_key":
            has_openai = re.search(r"`OPENAI_API_KEY`", readme_text)
            has_h4ck = re.search(r"`H4CKATH0N_OPENAI_API_KEY`", readme_text)
            if not has_openai and not has_h4ck:
                missing.append(field)
            continue

        combined = rf"`{env_var_name}`"
        if not re.search(combined, readme_text):
            missing.append(field)

    return missing


def main() -> int:
    fields = get_settings_fields()
    missing = check_env_vars_in_readme(fields)

    if missing:
        print("❌ The following configuration variables are NOT documented in README.md:\n")
        for field in missing:
            env_var_name = f"H4CKATH0N_{field.upper()}"
            print(f"  {env_var_name}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(fields)} configuration variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
