#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var in Settings is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Fix: Dynamically insert SRC_PATH to find local modules before importing them,
# otherwise "uv run scripts/check_env_vars.py" or just calling it may fail
# if the app isn't installed. We use # noqa: E402 on subsequent imports.
SRC_PATH = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_PATH))

from h4ckath0n.config import Settings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    readme_text = README.read_text()
    missing = []

    # Extract all documented variables from the Configuration table
    # Matches lines like: | `H4CKATH0N_ENV` | `development` | ...
    documented_vars = set()
    for line in readme_text.splitlines():
        match = re.match(r"^\|\s*`([A-Z0-9_]+)`\s*\|", line)
        if match:
            documented_vars.add(match.group(1))

    prefix = "H4CKATH0N_"
    # Access model_fields to avoid PydanticDeprecatedSince211 warnings
    for field_name in Settings.model_fields:
        env_name = f"{prefix}{field_name.upper()}"
        if env_name not in documented_vars:
            missing.append(env_name)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for var in missing:
            print(f"  {var}")
        print("\nPlease add them to the Configuration table in README.md.")
        return 1

    print("✅ All environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
