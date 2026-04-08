#!/usr/bin/env -S uv run python
"""Drift-prevention check and generator: update README.md config table.

Usage (from repo root):
    uv run scripts/generate_doc_config.py          # Updates README.md
    uv run scripts/generate_doc_config.py --check  # Fails if README.md is out of sync

The script imports the h4ckath0n app Settings, builds a markdown table using pydantic
Field descriptions, and injects it into README.md between <!-- CONFIG_TABLE_START -->
and <!-- CONFIG_TABLE_END --> markers.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_START = "<!-- CONFIG_TABLE_START -->"
MARKER_END = "<!-- CONFIG_TABLE_END -->"


def build_config_table() -> str:
    """Generate the markdown table for configuration settings."""
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    # We want to format the list defaults as `[]` instead of `[]` (they should be strings)
    # Actually, pydantic field.default or field.default_factory are used
    for field_name, field_info in Settings.model_fields.items():
        env_var_name = f"H4CKATH0N_{field_name.upper()}"

        # Determine the default value presentation
        if field_info.default_factory is not None:
            # Special handling for default_factory=list
            if field_info.default_factory is list:
                default_str = "`[]`"
            elif field_info.default_factory is dict:
                default_str = "`{}`"
            else:
                default_str = "empty"
        elif field_info.default is not None and field_info.default != "":
            if isinstance(field_info.default, bool):
                default_str = f"`{'true' if field_info.default else 'false'}`"
            else:
                default_str = f"`{field_info.default}`"
        else:
            default_str = "empty"

        description = field_info.description or ""

        lines.append(f"| `{env_var_name}` | {default_str} | {description} |")

    return "\n".join(lines)


def get_readme_parts(readme_text: str) -> tuple[str, str, str]:
    """Split the README into pre, table, and post parts based on markers."""
    start_idx = readme_text.find(MARKER_START)
    end_idx = readme_text.find(MARKER_END)

    if start_idx == -1 or end_idx == -1:
        print("❌ Could not find CONFIG_TABLE_START or CONFIG_TABLE_END markers in README.md.")
        sys.exit(1)

    end_idx += len(MARKER_END)

    pre = readme_text[: start_idx + len(MARKER_START)]
    table = readme_text[start_idx + len(MARKER_START) : end_idx - len(MARKER_END)].strip()
    post = readme_text[end_idx - len(MARKER_END) :]

    return pre, table, post


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or check README.md configuration table."
    )
    parser.add_argument("--check", action="store_true", help="Fail if README.md needs updating")
    args = parser.parse_args()

    readme_text = README.read_text()
    pre, current_table, post = get_readme_parts(readme_text)

    new_table = build_config_table()

    # Make sure we add a newline before and after the table to keep things clean
    new_content = f"{pre}\n{new_table}\n{post}"

    if args.check:
        if current_table != new_table:
            print(
                "❌ The configuration table in README.md is out of sync with "
                "src/h4ckath0n/config.py."
            )
            print("Run `uv run scripts/generate_doc_config.py` to update it.")
            return 1
        print("✅ The configuration table in README.md is up to date.")
        return 0

    if current_table != new_table:
        README.write_text(new_content)
        print("✅ README.md configuration table updated.")
    else:
        print("✅ README.md configuration table is already up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
