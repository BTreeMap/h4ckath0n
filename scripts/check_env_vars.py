#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable from Settings is documented.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    sys.path.insert(0, str(REPO_ROOT / "src"))  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    readme_text = README.read_text()

    missing = []
    for field_name in Settings.model_fields:
        if field_name == "openai_api_key":
            continue

        env_var = f"H4CKATH0N_{field_name.upper()}"
        if f"`{env_var}`" not in readme_text:
            missing.append(env_var)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for m in missing:
            print(f"  {m}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(
        f"✅ All {len(Settings.model_fields)} environment variables are documented in README.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
