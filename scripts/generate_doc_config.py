#!/usr/bin/env -S uv run python
"""Drift-prevention check: generate and verify README configuration table."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_TABLE_START -->"
END_MARKER = "<!-- CONFIG_TABLE_END -->"


def generate_table() -> str:
    from h4ckath0n.config import Settings  # noqa: E402

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for field_name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{field_name.upper()}"

        # Handle special LLM keys documented as empty
        if field_name == "openai_api_key":
            lines.append(f"| `OPENAI_API_KEY` | empty | {field_info.description} |")
            lines.append(
                f"| `H4CKATH0N_OPENAI_API_KEY` | empty | Alternate {field_info.description} |"
            )
            continue

        default_val = field_info.default
        if getattr(type(default_val), "__name__", "") == "PydanticUndefinedType":
            default_str = "required"
        elif default_val == "":
            default_str = "empty"
        elif default_val == []:
            default_str = "`[]`"
        elif isinstance(default_val, bool):
            default_str = f"`{'true' if default_val else 'false'}`"
        else:
            default_str = f"`{default_val}`"

        # Hardcode specific defaults for docs that are dynamic in code
        if field_name == "rp_id":
            default_str = "`localhost` in development"
        elif field_name == "origin":
            default_str = "`http://localhost:8000` in development"

        desc = field_info.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if the README is out of date")
    args = parser.parse_args()

    content = README.read_text()

    if START_MARKER not in content or END_MARKER not in content:
        print("❌ Could not find CONFIG_TABLE_START and CONFIG_TABLE_END in README.md")
        return 1

    start_idx = content.find(START_MARKER) + len(START_MARKER)
    end_idx = content.find(END_MARKER)

    table_md = generate_table()
    new_section = f"\n{table_md}\n"

    current_section = content[start_idx:end_idx]

    if current_section == new_section:
        if args.check:
            print("✅ Configuration table in README.md is up to date.")
        return 0

    if args.check:
        print(
            "❌ Configuration table in README.md is out of date. "
            "Run 'uv run scripts/generate_doc_config.py' to update it."
        )
        return 1

    new_content = content[:start_idx] + new_section + content[end_idx:]
    README.write_text(new_content)
    print("✨ Updated configuration table in README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
