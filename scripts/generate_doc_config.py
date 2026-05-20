#!/usr/bin/env -S uv run python
"""Drift-prevention script: generates the configuration table in README.md.

Usage (from repo root):
    uv run scripts/generate_doc_config.py          # Write to README.md
    uv run scripts/generate_doc_config.py --check  # Fail if README.md is out of sync
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Import Settings safely
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from h4ckath0n.config import Settings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_START = "<!-- CONFIG_TABLE_START -->"
MARKER_END = "<!-- CONFIG_TABLE_END -->"


def generate_table() -> str:
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        # Handle special cases if needed, but standard is H4CKATH0N_ + name.upper()
        env_var = f"H4CKATH0N_{name.upper()}"

        # Determine default representation
        if field.default == "":
            default_str = "empty"
        elif field.default is False:
            default_str = "`false`"
        elif field.default is True:
            default_str = "`true`"
        elif field.default == []:
            default_str = "`[]`"
        else:
            default_str = f"`{field.default}`"

        desc = field.description or ""
        lines.append(f"| `{env_var}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if README.md is up to date")
    args = parser.parse_args()

    readme_content = README.read_text()

    start_idx = readme_content.find(MARKER_START)
    end_idx = readme_content.find(MARKER_END)

    if start_idx == -1 or end_idx == -1:
        print(f"❌ Could not find {MARKER_START} or {MARKER_END} in README.md")
        return 1

    before = readme_content[: start_idx + len(MARKER_START)]
    after = readme_content[end_idx:]

    new_table = "\n" + generate_table() + "\n"
    new_readme_content = before + new_table + after

    if args.check:
        if readme_content != new_readme_content:
            print("❌ README.md configuration table is out of sync with Settings.")
            print("   Run `uv run scripts/generate_doc_config.py` to update it.")
            return 1
        else:
            print("✅ README.md configuration table is up to date.")
            return 0
    else:
        README.write_text(new_readme_content)
        print("✅ Updated README.md configuration table.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
