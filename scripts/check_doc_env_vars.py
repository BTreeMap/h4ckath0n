#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all configuration variables are documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py [--update]

The script generates a Markdown table of environment variables using the pydantic
Settings model fields and descriptions, and ensures that README.md has exactly this
table between the `<!-- BEGIN ENV VARS -->` and `<!-- END ENV VARS -->` markers.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_BEGIN = "<!-- BEGIN ENV VARS -->"
MARKER_END = "<!-- END ENV VARS -->"


def generate_env_table() -> str:
    lines = []
    lines.append("| Variable | Default | Description |")
    lines.append("|---|---|---|")

    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            desc = field.description or "OpenAI API key for the LLM wrapper"
            lines.append(f"| `OPENAI_API_KEY` | empty | {desc} |")
            lines.append(
                f"| `H4CKATH0N_OPENAI_API_KEY` | empty | Alternate OpenAI API key for the LLM wrapper |"
            )
            continue

        env_name = f"H4CKATH0N_{name.upper()}"

        # Use field.get_default() for Pydantic v2
        default_val = field.get_default()

        if default_val == "" or default_val is None:
            default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{str(default_val).lower()}`"
        elif isinstance(default_val, list):
            default_str = f"`{str(default_val)}`"
        else:
            default_str = f"`{default_val}`"

        desc = field.description or ""
        lines.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def check_or_update(update: bool = False) -> int:
    readme_text = README.read_text()

    if MARKER_BEGIN not in readme_text or MARKER_END not in readme_text:
        print(f"❌ Could not find {MARKER_BEGIN} or {MARKER_END} in README.md")
        return 1

    start_idx = readme_text.index(MARKER_BEGIN) + len(MARKER_BEGIN)
    end_idx = readme_text.index(MARKER_END)

    current_table = readme_text[start_idx:end_idx].strip()
    expected_table = generate_env_table().strip()

    if current_table == expected_table:
        print("✅ README.md environment variables are up-to-date.")
        return 0

    if update:
        new_text = readme_text[:start_idx] + "\n" + expected_table + "\n" + readme_text[end_idx:]
        README.write_text(new_text)
        print("✅ Updated README.md environment variables table.")
        return 0
    else:
        print("❌ README.md environment variables table is out-of-date.")
        print("Run `uv run scripts/check_doc_env_vars.py --update` to fix.")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update README.md inline")
    args = parser.parse_args()
    return check_or_update(args.update)


if __name__ == "__main__":
    sys.exit(main())
