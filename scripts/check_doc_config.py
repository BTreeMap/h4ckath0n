#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that configuration variables are documented.

Usage (from repo root):
    uv run scripts/check_doc_config.py
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
    for name, _field in Settings.model_fields.items():
        # OPENAI_API_KEY is an exception in the docs (no prefix)
        env_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            if "OPENAI_API_KEY" not in readme_text and env_name not in readme_text:
                missing.append(env_name)
        elif env_name not in readme_text:
            missing.append(env_name)

    # Validate that we also have the generated markers, to ensure they aren't removed
    if (
        "<!-- CONFIG_DOCS_START -->" not in readme_text
        or "<!-- CONFIG_DOCS_END -->" not in readme_text
    ):
        print(
            "❌ The CONFIG_DOCS_START and CONFIG_DOCS_END markers "
            "are missing from README.md. "
            "Please generate the config table using a script."
        )
        return 1

    if missing:
        print("❌ The following env vars are NOT documented in README.md:\n")
        for m in missing:
            print(f"  {m}")
        print("\nUpdate the 'Configuration' section in README.md to include them.")
        return 1

    print(f"✅ All {len(Settings.model_fields)} config vars are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
