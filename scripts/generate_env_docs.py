#!/usr/bin/env -S uv run python
"""Drift-prevention script: generate and check environment variable docs.

Usage:
    uv run scripts/generate_env_docs.py --update
    uv run scripts/generate_env_docs.py --check
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def generate_table() -> str:
    """Generate the markdown table of environment variables from Settings."""
    from h4ckath0n.config import Settings

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field in Settings.model_fields.items():
        env_var_name = f"H4CKATH0N_{name.upper()}"
        default = field.default

        if default == "":
            default_str = "empty"
        elif default == []:
            default_str = "`[]`"
        elif default is False:
            default_str = "`false`"
        elif default is True:
            default_str = "`true`"
        else:
            default_str = f"`{default}`"

        description = field.description or ""
        lines.append(f"| `{env_var_name}` | {default_str} | {description} |")

    return "\n".join(lines)


def update_readme(table_content: str) -> None:
    """Update the README with the generated table."""
    content = README.read_text(encoding="utf-8")

    if START_MARKER not in content or END_MARKER not in content:
        print(
            f"❌ Error: README.md is missing the {START_MARKER} or {END_MARKER} markers.",
            file=sys.stderr,
        )
        sys.exit(1)

    start_idx = content.find(START_MARKER) + len(START_MARKER)
    end_idx = content.find(END_MARKER)

    new_content = content[:start_idx] + "\n" + table_content + "\n" + content[end_idx:]
    README.write_text(new_content, encoding="utf-8")


def check_readme(table_content: str) -> bool:
    """Check if the README contains the up-to-date generated table."""
    content = README.read_text(encoding="utf-8")

    if START_MARKER not in content or END_MARKER not in content:
        print(
            f"❌ Error: README.md is missing the {START_MARKER} or {END_MARKER} markers.",
            file=sys.stderr,
        )
        return False

    start_idx = content.find(START_MARKER) + len(START_MARKER)
    end_idx = content.find(END_MARKER)

    current_table = content[start_idx:end_idx].strip()
    expected_table = table_content.strip()

    if current_table != expected_table:
        print("❌ Environment variables in README.md are out of date.")
        print("Run `uv run scripts/generate_env_docs.py --update` to fix.", file=sys.stderr)
        return False

    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate environment variable docs.")
    parser.add_argument("--update", action="store_true", help="Update README.md in place.")
    parser.add_argument("--check", action="store_true", help="Check if README.md is up to date.")
    args = parser.parse_args()

    if not args.update and not args.check:
        parser.print_help()
        return 1

    sys.path.insert(0, str(REPO_ROOT / "src"))
    table_content = generate_table()

    if args.update:
        update_readme(table_content)
        print("✅ README.md updated with latest environment variables.")
        return 0

    if args.check:
        if check_readme(table_content):
            print("✅ README.md environment variables are up to date.")
            return 0
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
