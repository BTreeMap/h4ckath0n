#!/usr/bin/env -S uv run python
"""Drift check: verify that config options in README.md are generated from the Settings model."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from pydantic_core import PydanticUndefined

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_expected_table() -> str:
    from h4ckath0n.config import Settings

    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            var_name = "H4CKATH0N_OPENAI_API_KEY"  # Also OPENAI_API_KEY

        default = field.default
        if default is PydanticUndefined:
            default = getattr(field, "default_factory", None)
            if default is not None:
                default = default()

        if default == "":
            default_str = "empty"
        elif isinstance(default, bool):
            default_str = f"`{str(default).lower()}`"
        elif default is None:
            default_str = "empty"
        else:
            default_str = f"`{default}`"

        desc = field.description or ""

        lines.append(f"| `{var_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    readme_text = README.read_text()

    start_marker = "<!-- BEGIN_CONFIG_TABLE -->"
    end_marker = "<!-- END_CONFIG_TABLE -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Configuration markers not found in README.md")
        return 1

    pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)
    current_table = pattern.search(readme_text).group(0)

    expected_table = f"{start_marker}\n{get_expected_table()}\n{end_marker}"

    if current_table.strip() != expected_table.strip():
        print("❌ Configuration table in README.md is out of date!")
        print("\nExpected:\n")
        print(expected_table)
        print("\nRun this script with --update to fix it.")

        if len(sys.argv) > 1 and sys.argv[1] == "--update":
            new_readme = readme_text.replace(current_table, expected_table)
            README.write_text(new_readme)
            print("✅ Updated README.md")
            return 0

        return 1

    print("✅ Configuration table is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
