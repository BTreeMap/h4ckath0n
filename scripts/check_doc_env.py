#!/usr/bin/env -S uv run python
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    from h4ckath0n.config import Settings

    readme_text = README.read_text()
    missing = []

    for field_name in Settings.model_fields:
        env_var = f"H4CKATH0N_{field_name.upper()}"

        # some exceptions:
        if field_name == "openai_api_key":
            if "OPENAI_API_KEY" not in readme_text and env_var not in readme_text:
                missing.append(env_var)
            continue

        if env_var not in readme_text:
            missing.append(env_var)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  {env_var}")
        print("\nAdd these variables to the Configuration table in README.md.")
        return 1

    print(
        f"✅ All {len(Settings.model_fields)} environment variables are documented in README.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
