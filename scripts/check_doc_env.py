#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that Pydantic Settings are documented.

Usage (from repo root):
    uv run scripts/check_doc_env.py

The script imports the application's configuration models and checks that
README.md mentions each corresponding environment variable enclosed in backticks.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[str]:
    from h4ckath0n.config import Settings
    from h4ckath0n.obs.settings import ObservabilitySettings

    env_vars = []

    settings_prefix = Settings.model_config.get("env_prefix", "")
    for key in Settings.model_fields:
        if key == "openai_api_key":
            env_vars.append("OPENAI_API_KEY")
            env_vars.append(f"{settings_prefix}OPENAI_API_KEY")
        else:
            env_vars.append(f"{settings_prefix}{key.upper()}")

    obs_prefix = ObservabilitySettings.model_config.get("env_prefix", "")
    for key in ObservabilitySettings.model_fields:
        env_vars.append(f"{obs_prefix}{key.upper()}")

    return env_vars


def main() -> int:
    readme_text = README.read_text()
    env_vars = get_env_vars()
    missing: list[str] = []

    for env_var in env_vars:
        # Strictly match the variable name enclosed in backticks to avoid
        # false-positive substring matches.
        if f"`{env_var}`" not in readme_text:
            missing.append(env_var)

    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  {env_var}")
        print("\nAdd these environment variables to the Configuration section in README.md.")
        return 1

    print(f"✅ All {len(env_vars)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
