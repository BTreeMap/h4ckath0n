#!/usr/bin/env -S uv run python
"""Drift-prevention check: generate configuration docs from the source of truth."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_TABLE_START -->"
END_MARKER = "<!-- CONFIG_TABLE_END -->"


def generate_table() -> str:
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        # Exclude H4CKATH0N_OPENAI_API_KEY to match README content
        if name == "h4ckath0n_openai_api_key":
            continue
        default_val = field.default
        is_undef = getattr(type(default_val), "__name__", "") == "PydanticUndefinedType"
        if is_undef or default_val == "":
            default_str = "empty"
        elif isinstance(default_val, list):
            default_str = "`[]`" if not default_val else f"`{json.dumps(default_val)}`"
        else:
            default_str = (
                str(default_val).lower() if isinstance(default_val, bool) else str(default_val)
            )
            default_str = f"`{default_str}`"

        env_var = "OPENAI_API_KEY" if name == "openai_api_key" else f"H4CKATH0N_{name.upper()}"
        desc = field.description or "No description"
        lines.append(f"| `{env_var}` | {default_str} | {desc} |")

    # Add H4CKATH0N_OPENAI_API_KEY explicitly
    lines.append(
        "| `H4CKATH0N_OPENAI_API_KEY` | empty | Alternate OpenAI API key for the LLM wrapper |"
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if README is up to date.")
    args = parser.parse_args()

    readme_content = README.read_text(encoding="utf-8")

    if START_MARKER not in readme_content or END_MARKER not in readme_content:
        print("❌ Markers not found in README.md", file=sys.stderr)
        return 1

    pattern = re.compile(f"{START_MARKER}.*?{END_MARKER}", re.DOTALL)
    new_table = f"{START_MARKER}\n{generate_table()}\n{END_MARKER}"

    match = pattern.search(readme_content)
    if not match:
        print("❌ Could not match markers in README.md", file=sys.stderr)
        return 1

    current_section = match.group(0)

    if args.check:
        if current_section != new_table:
            print(
                "❌ The configuration table in README.md is out of sync with config.py.",
                file=sys.stderr,
            )
            print(
                "Please run `uv run python scripts/generate_doc_config.py` to fix it.",
                file=sys.stderr,
            )
            return 1
        print("✅ Configuration table in README.md is up to date.")
        return 0

    if current_section != new_table:
        new_content = pattern.sub(new_table, readme_content)
        README.write_text(new_content, encoding="utf-8")
        print("✅ Updated configuration table in README.md.")
    else:
        print("✅ Configuration table in README.md is already up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
