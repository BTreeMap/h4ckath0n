#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every configuration variable is documented.

Usage (from repo root):
    uv run scripts/check_doc_config.py

The script imports the h4ckath0n config Settings, enumerates all fields, and checks
that README.md mentions each one (e.g. `H4CKATH0N_ENV`).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_config_fields() -> list[str]:
    """Return a list of configuration field names from Settings."""
    from h4ckath0n.config import Settings  # noqa: E402

    return list(Settings.model_fields.keys())


def check_fields_in_readme(fields: list[str]) -> list[str]:
    """Return field names that are not mentioned in README.md."""
    readme_text = README.read_text()
    missing: list[str] = []

    for field_name in fields:
        env_var = f"H4CKATH0N_{field_name.upper()}"

        # Special case for OpenAI API key which might be documented without prefix
        if env_var == "H4CKATH0N_OPENAI_API_KEY":
            if not re.search(r"`OPENAI_API_KEY`", readme_text) and not re.search(
                r"`H4CKATH0N_OPENAI_API_KEY`", readme_text
            ):
                missing.append(env_var)
            continue

        # Look for the exact env var name enclosed in backticks
        pattern = rf"`{env_var}`"
        if not re.search(pattern, readme_text):
            missing.append(env_var)

    return missing


def main() -> int:
    fields = get_config_fields()
    missing = check_fields_in_readme(fields)

    if missing:
        print("❌ The following configuration variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nAdd these variables to the Configuration section in README.md.")
        return 1

    print(f"✅ All {len(fields)} configuration variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
