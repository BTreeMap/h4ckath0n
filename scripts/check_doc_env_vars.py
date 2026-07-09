#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var in the config is documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

sys.path.insert(0, str(REPO_ROOT / "src"))

from h4ckath0n.config import Settings  # noqa: E402


def main() -> int:
    readme_text = README.read_text()
    missing: list[str] = []

    for name in Settings.model_fields:
        env_name = f"H4CKATH0N_{name.upper()}"
        if f"`{env_name}`" not in readme_text:
            missing.append(env_name)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for m in missing:
            print(f"  {m}")
        print("\nAdd these variables to the Configuration section in README.md.")
        return 1

    print("✅ All configuration environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
