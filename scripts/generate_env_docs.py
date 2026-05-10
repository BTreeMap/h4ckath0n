#!/usr/bin/env -S uv run python
"""Drift-prevention script to keep README.md environment variables in sync with config.py."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Import Settings to access its fields
from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def generate_markdown_table() -> str:
    """Generate the markdown table for configuration variables."""
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    # Process each field in Settings
    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"

        # Handle default values appropriately
        default_val = field.default
        if default_val == "":
            default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{str(default_val).lower()}`"
        elif isinstance(default_val, list):
            default_str = f"`{str(default_val)}`"
        elif isinstance(default_val, str):
            default_str = f"`{default_val}`"
        else:
            default_str = f"`{default_val}`"

        description = getattr(field, "description", None) or ""

        lines.append(f"| `{var_name}` | {default_str} | {description} |")

    return "\n".join(lines)


def update_readme(table: str) -> None:
    """Rewrite README.md with the new table."""
    content = README.read_text(encoding="utf-8")

    if START_MARKER not in content or END_MARKER not in content:
        print(
            f"Error: Could not find '{START_MARKER}' and '{END_MARKER}' markers in README.md",
            file=sys.stderr,
        )
        sys.exit(1)

    start_idx = content.find(START_MARKER) + len(START_MARKER)
    end_idx = content.find(END_MARKER)

    new_content = content[:start_idx] + "\n" + table + "\n" + content[end_idx:]
    README.write_text(new_content, encoding="utf-8")


def check_readme(table: str) -> bool:
    """Check if the README.md needs updating."""
    content = README.read_text(encoding="utf-8")

    if START_MARKER not in content or END_MARKER not in content:
        print(
            f"Error: Could not find '{START_MARKER}' and '{END_MARKER}' markers in README.md",
            file=sys.stderr,
        )
        sys.exit(1)

    start_idx = content.find(START_MARKER) + len(START_MARKER)
    end_idx = content.find(END_MARKER)

    current_table = content[start_idx:end_idx].strip()
    return current_table == table.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage environment variable docs.")
    parser.add_argument("--update", action="store_true", help="Update the README.md")
    parser.add_argument("--check", action="store_true", help="Check if README.md is up to date")
    args = parser.parse_args()

    if not args.update and not args.check:
        parser.print_help()
        return 1

    table = generate_markdown_table()

    if args.check:
        if not check_readme(table):
            print(
                "❌ README.md environment variables are out of sync with config.py.",
                file=sys.stderr,
            )
            print("Run 'uv run scripts/generate_env_docs.py --update' to fix.", file=sys.stderr)
            return 1
        print("✅ README.md environment variables are up to date.")
        return 0

    if args.update:
        update_readme(table)
        print("✅ README.md updated successfully.")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
