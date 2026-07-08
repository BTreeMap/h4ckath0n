#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every configuration variable in Settings is documented.

Usage (from repo root):
    uv run scripts/check_doc_config.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    from h4ckath0n.config import Settings  # noqa: E402

    readme_text = README.read_text(encoding="utf-8")
    missing: list[str] = []

    for key in Settings.model_fields:
        env_var_name = f"H4CKATH0N_{key.upper()}"
        if key == "openai_api_key":
            if not re.search(r"`OPENAI_API_KEY`", readme_text):
                missing.append("OPENAI_API_KEY")
            continue

        if not re.search(rf"`{env_var_name}`", readme_text):
            missing.append(env_var_name)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  {env_var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(
        f"✅ All {len(Settings.model_fields)} configuration variables are documented in README.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
