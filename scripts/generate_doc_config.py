#!/usr/bin/env -S uv run python
"""Drift-prevention check: generate the configuration table in README.md from config.py.

Usage (from repo root):
    uv run scripts/generate_doc_config.py [--check]

Reads Settings from src/h4ckath0n/config.py and injects a markdown table between
<!-- CONFIG_TABLE_START --> and <!-- CONFIG_TABLE_END --> markers in README.md.
If --check is provided, it fails if the README needs to be updated.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_TABLE_START -->"
END_MARKER = "<!-- CONFIG_TABLE_END -->"


def format_default(val: Any) -> str:
    """Format default value for markdown table."""
    if val == "":
        return "empty"
    if isinstance(val, bool):
        return f"`{'true' if val else 'false'}`"
    if isinstance(val, list):
        if not val:
            return "`[]`"
        return f"`{val}`"
    return f"`{val}`"


def generate_table() -> str:
    """Generate the markdown table for configuration settings."""
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        var_name = f"`H4CKATH0N_{name.upper()}`"
        # Special cases that don't have the H4CKATH0N_ prefix
        if name == "openai_api_key":
            var_name = "`OPENAI_API_KEY`"
        default_val = format_default(field.default)
        # Note: Some default logic in README.md doesn't map perfectly to python default values.
        # e.g., rp_id and origin, which have logic in the methods.
        if name == "rp_id":
            default_val = "`localhost` in development"
        elif name == "origin":
            default_val = "`http://localhost:8000` in development"

        desc = field.description or ""
        lines.append(f"| {var_name} | {default_val} | {desc} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Update or check README config table.")
    parser.add_argument("--check", action="store_true", help="Fail if update is required")
    args = parser.parse_args()

    table_md = generate_table()
    readme_text = README.read_text(encoding="utf-8")

    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        print(f"Error: {START_MARKER} and {END_MARKER} must exist in README.md", file=sys.stderr)
        return 1

    start_idx = readme_text.find(START_MARKER) + len(START_MARKER)
    end_idx = readme_text.find(END_MARKER)

    new_readme_text = readme_text[:start_idx] + "\n" + table_md + "\n" + readme_text[end_idx:]

    if readme_text == new_readme_text:
        print("✅ Configuration table is up to date.")
        return 0

    if args.check:
        print(
            "❌ README out of date. Run 'uv run scripts/generate_doc_config.py'.",
            file=sys.stderr,
        )
        return 1

    README.write_text(new_readme_text, encoding="utf-8")
    print("📝 Updated configuration table in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
