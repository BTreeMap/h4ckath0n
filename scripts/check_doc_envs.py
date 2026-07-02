#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var in Settings is documented.

Usage (from repo root):
    uv run scripts/check_doc_envs.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_envs() -> list[str]:
    from h4ckath0n.config import Settings

    envs = []
    for k in Settings.model_fields:
        if k == "openai_api_key":
            envs.append("OPENAI_API_KEY")
        else:
            envs.append(f"H4CKATH0N_{k.upper()}")
    return sorted(envs)


def check_envs_in_readme(envs: list[str]) -> list[str]:
    readme_text = README.read_text()
    missing = []
    for env in envs:
        if f"`{env}`" not in readme_text:
            missing.append(env)
    return missing


def main() -> int:
    envs = get_settings_envs()
    missing = check_envs_in_readme(envs)

    if missing:
        print("❌ The following env vars are NOT documented in README.md:\n")
        for env in missing:
            print(f"  {env}")
        return 1

    print(f"✅ All {len(envs)} env vars are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
