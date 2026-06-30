#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify every config var in Settings is in README.md."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_keys() -> list[str]:
    from h4ckath0n.config import Settings

    return list(Settings.model_fields.keys())


def main() -> int:
    keys = get_settings_keys()
    readme_text = README.read_text()

    missing = []
    for key in keys:
        env_var = f"H4CKATH0N_{key.upper()}"
        if env_var not in readme_text:
            if key == "openai_api_key" and "OPENAI_API_KEY" in readme_text:
                continue
            missing.append(env_var)

    if missing:
        print("❌ The following config variables are NOT documented in README.md:\n")
        for m in missing:
            print(f"  `{m}`")
        print("\nPlease add them to the Configuration section in README.md.")
        return 1

    print(f"✅ All {len(keys)} config variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
