#!/usr/bin/env -S uv run python
"""Drift-prevention check: generate the configuration table from source code.

This script parses src/h4ckath0n/config.py, extracts the configuration settings,
and injects them into README.md between the <!-- CONFIG_TABLE_START --> and
<!-- CONFIG_TABLE_END --> markers. If run with --check, it fails if the file
would change.
"""

import argparse
import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_TABLE_START -->"
END_MARKER = "<!-- CONFIG_TABLE_END -->"


def generate_table() -> str:
    """Generate the markdown table for settings."""
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            var_name = "`OPENAI_API_KEY`<br>`H4CKATH0N_OPENAI_API_KEY`"
        else:
            var_name = f"`H4CKATH0N_{name.upper()}`"

        default = field.default
        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"
        elif default == "":
            default_str = "empty"
        elif default is False:
            default_str = "`false`"
        elif default is True:
            default_str = "`true`"
        elif isinstance(default, list):
            default_str = "`[]`"
        else:
            default_str = f"`{default}`"

        desc = field.description or ""
        lines.append(f"| {var_name} | {default_str} | {desc} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if README needs updating")
    args = parser.parse_args()

    table = generate_table()
    content = README.read_text()

    if START_MARKER not in content or END_MARKER not in content:
        print("❌ README.md is missing CONFIG_TABLE_START or END_MARKER.", file=sys.stderr)
        return 1

    start_idx = content.find(START_MARKER) + len(START_MARKER)
    end_idx = content.find(END_MARKER)

    new_content = content[:start_idx] + "\n" + table + "\n" + content[end_idx:]

    if content == new_content:
        print("✅ README.md configuration table is up-to-date.")
        return 0

    if args.check:
        print(
            "❌ README.md configuration table is out-of-date. Run "
            "scripts/generate_doc_config.py to update it.",
            file=sys.stderr,
        )
        return 1

    README.write_text(new_content)
    print("✅ README.md configuration table updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
