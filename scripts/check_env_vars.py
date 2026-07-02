#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all configuration settings in Settings
are documented in README.md.

Usage (from repo root):
    uv run scripts/check_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from h4ckath0n.config import Settings  # noqa: E402

    # Avoid instantiation side-effects in tests by using model_fields.
    fields = Settings.model_fields
    readme_text = README.read_text()

    missing: list[str] = []
    for field_name in fields:
        env_var = f"H4CKATH0N_{field_name.upper()}"

        # Special case: the app checks OPENAI_API_KEY as well as H4CKATH0N_OPENAI_API_KEY
        if env_var == "H4CKATH0N_OPENAI_API_KEY":
            if "OPENAI_API_KEY" not in readme_text:
                missing.append("OPENAI_API_KEY")
            if env_var not in readme_text:
                missing.append(env_var)
            continue

        if f"`{env_var}`" not in readme_text:
            missing.append(env_var)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  {env_var}")
        print("\nAdd these variables to the Configuration section in README.md.")
        return 1

    print(f"✅ All {len(fields)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
