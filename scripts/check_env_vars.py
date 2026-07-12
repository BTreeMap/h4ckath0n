#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every Settings field is documented."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def check_env_vars() -> int:
    from h4ckath0n.config import Settings

    readme_text = README.read_text()
    missing = []
    for field in Settings.model_fields:
        env_name = f"H4CKATH0N_{field.upper()}"
        if field == "openai_api_key":
            if "OPENAI_API_KEY" not in readme_text:
                missing.append("OPENAI_API_KEY")
        else:
            if env_name not in readme_text:
                missing.append(env_name)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for m in missing:
            print(f"  {m}")
        return 1
    print(
        f"✅ All {len(Settings.model_fields)} environment variables are documented in README.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(check_env_vars())
