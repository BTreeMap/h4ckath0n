#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var in h4ckath0n.config is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    readme_text = README.read_text()

    missing = []

    # We prefix with H4CKATH0N_ unless field explicitly overrides it
    prefix = Settings.model_config.get("env_prefix", "H4CKATH0N_")

    for field_name in Settings.model_fields:
        env_var = f"{prefix}{field_name}".upper()

        # Check if the env_var is mentioned in the table in README
        # Look for it wrapped in backticks
        if not re.search(rf"`{env_var}`", readme_text):
            missing.append(env_var)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  {env_var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(
        f"✅ All {len(Settings.model_fields)} environment variables are documented in README.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
