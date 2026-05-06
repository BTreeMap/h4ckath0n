#!/usr/bin/env -S uv run python
"""Drift-prevention script to generate environment variable documentation.

Usage:
    uv run scripts/generate_env_docs.py --check
    uv run scripts/generate_env_docs.py --update
"""

import argparse
import re
import sys
from pathlib import Path

# Add src to sys.path so we can import h4ckath0n
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def generate_markdown_table() -> str:
    """Generate a markdown table from Settings fields."""
    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    # We want to iterate through the model fields to document them
    for name, field in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"

        # Determine the default value correctly
        if getattr(field, "default_factory", None) is not None:
            # We use repr() on an instance of the default_factory to get `[]` or `{}`
            default_val = field.default_factory()
            default = f"`{repr(default_val)}`"
        elif field.default is not None:
            default_val = field.default
            if isinstance(default_val, bool):
                default = "`true`" if default_val else "`false`"
            elif default_val == "":
                default = "empty"
            else:
                default = f"`{default_val}`"
        else:
            default = "empty"

        desc = field.description or ""
        lines.append(f"| `{env_name}` | {default} | {desc} |")

    return "\n".join(lines)


def update_readme(new_table: str) -> None:
    """Update README.md with the new environment variables table."""
    content = README.read_text()

    pattern = re.compile(rf"{START_MARKER}.*?{END_MARKER}", re.DOTALL)
    new_content = pattern.sub(f"{START_MARKER}\n{new_table}\n{END_MARKER}", content)

    README.write_text(new_content)


def check_readme(new_table: str) -> bool:
    """Check if README.md is up-to-date with the environment variables table."""
    content = README.read_text()
    pattern = re.compile(rf"{START_MARKER}\n(.*?)\n{END_MARKER}", re.DOTALL)
    match = pattern.search(content)

    if not match:
        print("❌ Markers not found in README.md")
        return False

    current_table = match.group(1).strip()
    new_table_stripped = new_table.strip()

    if current_table != new_table_stripped:
        print("❌ Environment variables documentation is out of date.")
        print("Run `uv run scripts/generate_env_docs.py --update` to fix it.")
        return False

    print("✅ Environment variables documentation is up to date.")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if README.md is up-to-date")
    parser.add_argument("--update", action="store_true", help="Update README.md inline")
    args = parser.parse_args()

    table = generate_markdown_table()

    if args.update:
        update_readme(table)
        print("✅ README.md updated.")
    elif args.check:
        if not check_readme(table):
            sys.exit(1)
    else:
        print("Use --check or --update")
