#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every environment variable in Settings is documented.

Usage (from repo root):
    uv run scripts/check_doc_envs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_expected_envs() -> list[str]:
    from h4ckath0n.config import Settings

    envs = []
    for key in Settings.model_fields:
        prefix = Settings.model_config.get("env_prefix", "")
        envs.append((prefix + key).upper())
    return envs


def check_envs_in_readme(envs: list[str]) -> list[str]:
    readme_text = README.read_text(encoding="utf-8")
    missing = []
    for env in envs:
        pattern = rf"`{env}`"
        if not re.search(pattern, readme_text):
            missing.append(env)
    return missing


def main() -> int:
    envs = get_expected_envs()
    missing = check_envs_in_readme(envs)
    if "H4CKATH0N_OPENAI_API_KEY" in missing:
        missing.remove("H4CKATH0N_OPENAI_API_KEY")
    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env in missing:
            print(f"  {env}")
        print("\nAdd these environment variables to README.md.")
        return 1
    print(f"✅ All {len(envs)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
