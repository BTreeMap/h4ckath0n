#!/usr/bin/env -S uv run python
"""Drift-prevention generator: keep the Configuration table in README.md up to date.

This script parses src/h4ckath0n/config.py and extracts all `pydantic.Field`
descriptions and defaults (if present). It then injects a Markdown table
between `<!-- CONFIG_TABLE_START -->` and `<!-- CONFIG_TABLE_END -->` markers
in the README.md.

Run with `--check` to fail if the README.md is out of sync.
"""

import argparse
import json
import sys
from pathlib import Path

from pydantic_core import PydanticUndefined

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_TABLE_START -->\n"
END_MARKER = "<!-- CONFIG_TABLE_END -->\n"


def format_default(val) -> str:
    if val == "":
        return "empty"
    if val is PydanticUndefined:
        return "`[]`"
    if isinstance(val, bool):
        return f"`{'true' if val else 'false'}`"
    if isinstance(val, (list, dict)):
        return f"`{json.dumps(val)}`"
    return f"`{val}`"


def generate_table() -> str:
    from h4ckath0n.config import Settings

    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"
        default_val = format_default(field.default)
        desc = field.description or ""

        # Override special cases for backward compat
        if name == "openai_api_key":
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
            lines.append(
                "| `H4CKATH0N_OPENAI_API_KEY` | empty | "
                "Alternate OpenAI API key for the LLM wrapper |"
            )
            continue

        lines.append(f"| `{env_name}` | {default_val} | {desc} |")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    content = README.read_text()
    if START_MARKER not in content or END_MARKER not in content:
        print("❌ Markers not found in README.md")
        return 1

    before = content.split(START_MARKER)[0]
    after = content.split(END_MARKER)[1]

    new_table = generate_table()
    new_content = f"{before}{START_MARKER}{new_table}{END_MARKER}{after}"

    if args.check:
        if content != new_content:
            print("❌ Configuration table in README.md is out of sync.")
            print("Run `uv run scripts/generate_doc_config.py` to update it.")
            return 1
        print("✅ Configuration table is up to date.")
        return 0

    README.write_text(new_content)
    print("✅ Configuration table updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
