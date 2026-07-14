#!/usr/bin/env -S uv run python
"""Verify that every ``Settings`` environment variable is documented in the README."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
_DOCUMENTED_ENVIRONMENT = re.compile(r"^\|\s*`([A-Z][A-Z0-9_]*)`\s*\|", re.MULTILINE)


def get_settings_environment_names() -> frozenset[str]:
    """Return the environment variable name for each Settings field."""
    from h4ckath0n.config import Settings

    return frozenset(f"H4CKATH0N_{field_name.upper()}" for field_name in Settings.model_fields)


def get_documented_environment_names(readme_text: str) -> frozenset[str]:
    """Return environment variable names from the first column of README tables."""
    return frozenset(_DOCUMENTED_ENVIRONMENT.findall(readme_text))


def main() -> int:
    documented = get_documented_environment_names(README.read_text())
    missing = sorted(get_settings_environment_names().difference(documented))
    if missing:
        print("The following environment variables are not documented in README.md:\n")
        for environment_name in missing:
            print(f"  {environment_name}")
        return 1

    environment_count = len(get_settings_environment_names())
    print(f"All {environment_count} Settings environment variables are documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
