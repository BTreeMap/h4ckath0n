#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables in README.md match config.py.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py [--update]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
MARKER_START = "<!-- ENV_VARS_START -->\n"
MARKER_END = "<!-- ENV_VARS_END -->\n"


def generate_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        default = field.default
        if default == "":
            default_str = "empty"
        elif default == []:
            default_str = "`[]`"
        elif isinstance(default, bool):
            default_str = f"`{str(default).lower()}`"
        elif isinstance(default, str) and "sqlite" in default:
            default_str = f"`{default}`"
        elif default == "localhost":
            default_str = "`localhost` in development"
        elif default == "http://localhost:8000":
            default_str = "`http://localhost:8000` in development"
        elif isinstance(default, str):
            default_str = f"`{default}`"
        else:
            default_str = f"`{default}`"
        desc = field.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {desc} |")
    # also add the alternate openai one manually as it's not a field
    lines.append("| `OPENAI_API_KEY` | empty | Alternate OpenAI API key for the LLM wrapper |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    readme_text = README.read_text()
    if MARKER_START not in readme_text or MARKER_END not in readme_text:
        print("❌ Markers not found in README.md.")
        return 1

    start_idx = readme_text.index(MARKER_START) + len(MARKER_START)
    end_idx = readme_text.index(MARKER_END)

    current_table = readme_text[start_idx:end_idx]
    expected_table = generate_table()

    if current_table == expected_table:
        print("✅ Environment variables in README.md are up to date.")
        return 0

    if args.update:
        new_text = readme_text[:start_idx] + expected_table + readme_text[end_idx:]
        README.write_text(new_text)
        print("✅ Updated environment variables in README.md.")
        return 0
    else:
        print("❌ Environment variables in README.md are out of date.")
        print("Run 'uv run scripts/check_doc_env_vars.py --update' to fix.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
