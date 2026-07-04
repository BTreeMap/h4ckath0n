#!/usr/bin/env -S uv run python
"""Drift check: verify that every environment variable in the Settings class is documented.

Usage (from repo root):
    uv run scripts/check_doc_envs.py

The script imports the Settings model, enumerates all fields, and checks that
README.md mentions each one. Settings intended for internal framework usage
can be excluded via FRAMEWORK_ENVS.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# Settings that we intentionally omit from documentation.
FRAMEWORK_ENVS = frozenset({"H4CKATH0N_DEMO_MODE"})


def get_app_envs() -> list[str]:
    """Return environment variable names from the live Settings model."""
    from h4ckath0n.config import Settings  # noqa: E402

    envs: list[str] = []
    for field_name in Settings.model_fields:
        env_var = "H4CKATH0N_" + field_name.upper()
        if env_var in FRAMEWORK_ENVS:
            continue
        envs.append(env_var)
    return sorted(envs)


def check_envs_in_readme(envs: list[str]) -> list[str]:
    """Return env vars that are not mentioned as code blocks in README.md."""
    readme_text = README.read_text()
    missing: list[str] = []
    for env in envs:
        # OPENAI_API_KEY is an exception that is documented directly
        if env == "H4CKATH0N_OPENAI_API_KEY":
            if "OPENAI_API_KEY" not in readme_text:
                missing.append(env)
            continue

        # Ensure it appears as a code block (e.g. `H4CKATH0N_ENV`)
        if f"`{env}`" not in readme_text:
            missing.append(env)
    return missing


def main() -> int:
    envs = get_app_envs()
    missing = check_envs_in_readme(envs)

    if missing:
        print("❌ The following env vars are NOT documented in README.md:\n")
        for env in missing:
            print(f"  {env}")
        print(
            "\nAdd these to the Configuration section in README.md or, "
            "if intentionally undocumented, add them to FRAMEWORK_ENVS in this script."
        )
        return 1

    print(f"✅ All {len(envs)} environment variables are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
