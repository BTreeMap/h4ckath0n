#!/usr/bin/env python3
"""Drift-prevention check: verify that every configuration setting is documented.

Usage (from repo root):
    uv run scripts/check_doc_config.py

The script imports the h4ckath0n config Settings, enumerates all fields, and checks that
README.md mentions each one.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_config_fields() -> list[str]:
    """Return a list of environment variable names expected by Settings."""
    from h4ckath0n.config import Settings  # noqa: E402

    fields = []
    prefix = Settings.model_config.get("env_prefix", "H4CKATH0N_").upper()
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            fields.append("OPENAI_API_KEY")
            fields.append(f"{prefix}OPENAI_API_KEY")
        else:
            fields.append(f"{prefix}{field_name.upper()}")

    return fields


def check_config_in_readme(fields: list[str]) -> list[str]:
    """Return fields that are not mentioned anywhere in README.md."""
    readme_text = README.read_text()
    missing: list[str] = []
    for field in fields:
        # Check if the field name is mentioned in the README
        if not re.search(rf"`{field}`", readme_text):
            missing.append(field)
    return missing


def main() -> int:
    fields = get_config_fields()

    missing = check_config_in_readme(fields)

    if missing:
        print("❌ The following configuration variables are NOT documented in README.md:\n")
        for field in missing:
            print(f"  {field}")
        print("\nAdd these variables to the Configuration section in README.md.")
        return 1

    print(f"✅ All {len(fields)} configuration variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
