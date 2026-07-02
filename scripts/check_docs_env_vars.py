#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all environment variables are documented in README.md.

Usage (from repo root):
    uv run scripts/check_docs_env_vars.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    from h4ckath0n.config import Settings  # noqa: E402

    settings_fields = Settings.model_fields

    readme_text = README.read_text(encoding="utf-8")

    missing: list[str] = []

    for field_name in settings_fields:
        if field_name == "openai_api_key":
            if (
                "`OPENAI_API_KEY`" not in readme_text
                and "`H4CKATH0N_OPENAI_API_KEY`" not in readme_text
            ):
                missing.append("OPENAI_API_KEY")
        else:
            env_var = "H4CKATH0N_" + field_name.upper()
            if f"`{env_var}`" not in readme_text:
                missing.append(env_var)

    if missing:
        print("❌ The following environment variables are missing from README.md:\n")
        for m in missing:
            print(f"  {m}")
        print("\nPlease add them to the Configuration table in README.md.")
        return 1

    print(f"✅ All {len(settings_fields)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
