#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that configuration options in README.md match code.

Usage (from repo root):
    uv run scripts/generate_doc_config.py [--check]

This script imports the h4ckath0n app settings, enumerates all fields, and
updates the Configuration table in README.md. If --check is passed, it fails if
the file would change.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_config_table() -> str:
    from h4ckath0n.config import Settings  # noqa: E402

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field_info in Settings.model_fields.items():
        # Handle default value safely avoiding literal "PydanticUndefined"
        default = field_info.default
        is_undefined = getattr(type(default), "__name__", "") == "PydanticUndefinedType"

        if is_undefined or default == "":
            default_str = "empty"
        elif default == []:
            default_str = "`[]`"
        elif isinstance(default, bool):
            default_str = f"`{str(default).lower()}`"
        else:
            default_str = f"`{default}`"

        desc = field_info.description or ""
        var_name = f"`H4CKATH0N_{name.upper()}`"

        # Exceptions for specific env vars
        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"
        elif name == "openai_api_key":
            var_name = "`OPENAI_API_KEY`"

        lines.append(f"| {var_name} | {default_str} | {desc} |")

        # Hardcode H4CKATH0N_OPENAI_API_KEY explicitly since it's an alternate
        if name == "openai_api_key":
            lines.append(
                "| `H4CKATH0N_OPENAI_API_KEY` | empty | "
                "Alternate OpenAI API key for the LLM wrapper |"
            )

    return "\n".join(lines)


def update_readme(new_table: str, check_only: bool = False) -> int:
    readme_text = README.read_text()

    start_marker = "<!-- CONFIG_TABLE_START -->"
    end_marker = "<!-- CONFIG_TABLE_END -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print(f"❌ Could not find {start_marker} and {end_marker} in README.md")
        return 1

    start_idx = readme_text.index(start_marker) + len(start_marker)
    end_idx = readme_text.index(end_marker)

    new_readme = readme_text[:start_idx] + "\n" + new_table + "\n" + readme_text[end_idx:]

    if readme_text == new_readme:
        print("✅ README.md configuration table is up-to-date.")
        return 0

    if check_only:
        print("❌ README.md configuration table is out-of-date.")
        print("Run `uv run scripts/generate_doc_config.py` to update it.")
        return 1

    README.write_text(new_readme)
    print("✅ Updated README.md configuration table.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if README.md is up-to-date")
    args = parser.parse_args()

    table = generate_config_table()
    return update_readme(table, check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
