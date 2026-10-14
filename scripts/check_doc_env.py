#!/usr/bin/env -S uv run python
"""Verify that every ``Settings`` environment variable is documented in the README."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_expected_table() -> str:
    from h4ckath0n.config import Settings

    lines = []
    lines.append("| Variable | Default | Description |")
    lines.append("|---|---|---|")

    for name, field in Settings.model_fields.items():
        env_names = []
        if field.validation_alias:
            if isinstance(field.validation_alias, str):
                env_names = [field.validation_alias]
            else:
                env_names = [choice for choice in field.validation_alias.choices]
        else:
            env_names = [f"H4CKATH0N_{name.upper()}"]

        default_str = str(field.default)
        if isinstance(field.default, bool):
            default_str = str(field.default).lower()
        elif default_str == "":
            default_str = "empty"
        elif isinstance(field.default, list) or (
            hasattr(field, "default_factory") and field.default_factory is list
        ):
            default_str = "[]"

        if default_str not in ["empty", "[]"]:
            default_str = f"`{default_str}`"

        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"

        for env_name in env_names:
            desc = field.description or ""
            lines.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    readme_text = README.read_text()
    expected_table = generate_expected_table()

    start_marker = "<!-- START_ENV_VARS -->"
    end_marker = "<!-- END_ENV_VARS -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print(
            "Error: Missing <!-- START_ENV_VARS --> or <!-- END_ENV_VARS --> in README.md"
        )
        return 1

    start_idx = readme_text.find(start_marker) + len(start_marker)
    end_idx = readme_text.find(end_marker)

    actual_table = readme_text[start_idx:end_idx].strip()

    if actual_table != expected_table:
        print(
            "Error: README.md environment variables table is out of sync with Settings."
        )
        print("Run scripts/generate_env_docs.py to update it.")
        return 1

    print("All Settings environment variables are documented and synchronized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
