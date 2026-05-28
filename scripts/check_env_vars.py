#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var in Settings is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    from h4ckath0n.config import Settings

    readme_text = README.read_text()

    missing: list[str] = []
    # Use model_fields on the class to avoid deprecation warnings
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            env_vars = ["OPENAI_API_KEY", "H4CKATH0N_OPENAI_API_KEY"]
        else:
            env_vars = [f"H4CKATH0N_{field_name.upper()}"]

        found = any(env_var in readme_text for env_var in env_vars)
        if not found:
            missing.append(env_vars[0])

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  `{env_var}`")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(
        f"✅ All {len(Settings.model_fields)} environment variables "
        "from Settings are documented in README.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
