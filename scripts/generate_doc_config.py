#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that README.md configuration matches the codebase.

Usage (from repo root):
    uv run scripts/generate_doc_config.py [--check]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Fix to import correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from h4ckath0n.config import Settings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_TABLE_START -->\n"
END_MARKER = "<!-- CONFIG_TABLE_END -->\n"


def generate_table() -> str:
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        var_name = f"`H4CKATH0N_{name.upper()}`"

        default_val = field.default
        if not field.is_required() and field.default_factory:
            default_str = (
                "`[]`" if field.default_factory is list else f"`{field.default_factory()}`"
            )
        elif field.is_required():
            default_str = "required"
        elif name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"
        elif default_val == "" or default_val is None:
            default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{'true' if default_val else 'false'}`"
        elif isinstance(default_val, list):
            default_str = "`[]`" if not default_val else f"`{default_val}`"
        else:
            default_str = f"`{default_val}`"

        desc = field.description or ""

        if name == "openai_api_key":
            lines.append(
                f"| `OPENAI_API_KEY` | {default_str} | OpenAI API key for the LLM wrapper |"
            )
            lines.append(
                f"| `H4CKATH0N_OPENAI_API_KEY` | {default_str} | "
                "Alternate OpenAI API key for the LLM wrapper |"
            )
        else:
            lines.append(f"| {var_name} | {default_str} | {desc} |")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    readme_content = README.read_text(encoding="utf-8")

    if START_MARKER not in readme_content or END_MARKER not in readme_content:
        print(f"❌ Could not find {START_MARKER.strip()} or {END_MARKER.strip()} in README.md")
        return 1

    start_idx = readme_content.find(START_MARKER) + len(START_MARKER)
    end_idx = readme_content.find(END_MARKER)

    current_table = readme_content[start_idx:end_idx]
    new_table = generate_table()

    if args.check:
        if current_table != new_table:
            print("❌ README.md configuration table is out of sync with code.")
            print("Run `uv run scripts/generate_doc_config.py` to update it.")
            return 1
        print("✅ README.md configuration table is up to date.")
        return 0
    else:
        new_readme = readme_content[:start_idx] + new_table + readme_content[end_idx:]
        README.write_text(new_readme, encoding="utf-8")
        print("✅ Updated README.md configuration table.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
