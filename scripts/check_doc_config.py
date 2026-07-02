#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every config variable is documented."""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings():
    from h4ckath0n.config import Settings

    return Settings.model_fields.keys()


def check_settings_in_readme(settings):
    readme_text = README.read_text()
    missing = []
    for setting in settings:
        env_var = f"H4CKATH0N_{setting.upper()}"
        if setting == "openai_api_key":
            if not re.search(r"`OPENAI_API_KEY`", readme_text) and not re.search(
                r"`H4CKATH0N_OPENAI_API_KEY`", readme_text
            ):
                missing.append(env_var)
            continue

        if not re.search(rf"`{env_var}`", readme_text):
            missing.append(env_var)

    return missing


if __name__ == "__main__":
    settings = get_settings()
    missing = check_settings_in_readme(settings)
    if missing:
        print("❌ The following config variables are NOT documented in README.md:\n")
        for m in missing:
            print(f"  {m}")
        sys.exit(1)
    print("✅ All config variables are documented in README.md.")
    sys.exit(0)
