#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in Settings is documented.

Usage (from repo root):
    uv run scripts/check_doc_env.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    from h4ckath0n.config import Settings

    readme_text = README.read_text()
    missing = []

    # We iterate over the dictionary directly to avoid SIM118
    for field_name in Settings.model_fields:
        if field_name == "env":
            env_name = "H4CKATH0N_ENV"
        else:
            env_name = f"H4CKATH0N_{field_name.upper()}"

        if env_name not in readme_text:
            missing.append(env_name)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_name in missing:
            print(f"  {env_name}")
        print("\nAdd these to the Configuration section in README.md.")
        return 1

    print(
        f"✅ All {len(Settings.model_fields)} environment variables are documented in README.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
