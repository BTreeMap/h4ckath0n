#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables are documented."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def generate_env_table() -> str:
    """Generate markdown table of environment variables from Settings."""
    from h4ckath0n.config import Settings

    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in Settings.model_fields.items():
        # Handle prefix
        prefix = Settings.model_config.get("env_prefix", "")
        env_var = f"{prefix}{name}".upper()

        # Handle default
        if field.is_required():
            default_str = "*Required*"
        elif field.default_factory is not None:
            default_str = "*Dynamic*"
        else:
            default_val = field.default
            if default_val == "":
                default_str = "empty"
            elif default_val == []:
                default_str = "`[]`"
            elif isinstance(default_val, bool):
                default_str = f"`{'true' if default_val else 'false'}`"
            else:
                default_str = f"`{default_val}`"

        # Handle description
        description = field.description or ""

        lines.append(f"| `{env_var}` | {default_str} | {description} |")

    return "\n".join(lines)


def update_readme(new_table: str) -> bool:
    """Update README.md with the new table. Returns True if changed."""
    text = README.read_text()

    start_idx = text.find(START_MARKER)
    end_idx = text.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print(f"❌ Markers {START_MARKER} or {END_MARKER} not found in README.md")
        sys.exit(1)

    before = text[: start_idx + len(START_MARKER)]
    after = text[end_idx:]

    new_text = f"{before}\n{new_table}\n{after}"

    if new_text != text:
        README.write_text(new_text)
        return True
    return False


def check_readme(new_table: str) -> bool:
    """Check if README.md has the current table."""
    text = README.read_text()

    start_idx = text.find(START_MARKER)
    end_idx = text.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print(f"❌ Markers {START_MARKER} or {END_MARKER} not found in README.md")
        return False

    current_table = text[start_idx + len(START_MARKER) : end_idx].strip()

    if current_table != new_table.strip():
        print("❌ README.md environment variables table is out of date.")
        print("Run with --update to fix.")
        return False

    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update README.md inline")
    args = parser.parse_args()

    new_table = generate_env_table()

    if args.update:
        if update_readme(new_table):
            print("✅ Updated README.md with current environment variables.")
        else:
            print("✅ README.md is already up to date.")
        return 0
    else:
        if check_readme(new_table):
            print("✅ README.md environment variables table is up to date.")
            return 0
        return 1


if __name__ == "__main__":
    sys.exit(main())
