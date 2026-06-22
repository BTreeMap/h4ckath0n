#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var in Settings is documented.

Usage (from repo root):
    uv run scripts/check_config_drift.py
"""

import sys
from pathlib import Path


def main() -> int:
    from h4ckath0n.config import Settings

    env_vars = []
    # Avoid Pydantic V2.11 deprecation warning by accessing model_fields on the class directly
    for name in Settings.model_fields:
        env_vars.append(f"`H4CKATH0N_{name.upper()}`")  # Check for exact string in backticks

    docs_dir = Path("docs")
    found = set()
    for md_file in docs_dir.glob("**/*.md"):
        content = md_file.read_text()
        for env_var in env_vars:
            if env_var in content:
                found.add(env_var)

    readme = Path("README.md").read_text()
    for env_var in env_vars:
        if env_var in readme:
            found.add(env_var)

    missing = set(env_vars) - found
    if missing:
        print("❌ The following environment variables are NOT documented in docs/ or README.md:\n")
        for v in sorted(missing):
            print(f"  {v}")
        print("\nPlease document them or add a configuration index page.")
        return 1

    print(f"✅ All {len(env_vars)} environment variables are documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
