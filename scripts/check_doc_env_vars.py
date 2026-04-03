#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables are documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py [--update]

The script imports the h4ckath0n settings, enumerates all fields, and checks that
README.md has an up-to-date table.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[tuple[str, str, str]]:
    """Return (env_var_name, default, description) from Settings."""
    from h4ckath0n.config import Settings

    env_vars = []
    # Note: We need to pull from model_fields directly to get python defaults correctly
    for field_name, field_info in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{field_name.upper()}"
        if field_name == "openai_api_key":
            # openai_api_key might be H4CKATH0N_OPENAI_API_KEY but also just OPENAI_API_KEY
            pass

        default = ""
        if not field_info.is_required():
            # Handle dynamic defaults if any, but mostly static
            val = field_info.default
            if val is not None and val != "":
                if isinstance(val, list):
                    default = str(val).replace("'", '"')
                elif isinstance(val, bool):
                    default = str(val).lower()
                else:
                    default = str(val)
            elif val == "":
                default = "empty"
            else:
                default = ""

        desc = field_info.description or ""
        env_vars.append((env_name, default, desc))

    return env_vars


def generate_table(env_vars: list[tuple[str, str, str]]) -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for env_name, default, desc in env_vars:
        if env_name == "H4CKATH0N_OPENAI_API_KEY":
            # Special case based on existing docs
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
            lines.append(
                f"| `{env_name}` | {default or 'empty'} "
                "| Alternate OpenAI API key for the LLM wrapper |"
            )
        else:
            default_str = f"`{default}`" if default and default != "empty" else default
            lines.append(f"| `{env_name}` | {default_str} | {desc} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    env_vars = get_env_vars()
    table = generate_table(env_vars)

    readme_text = README.read_text()

    pattern = re.compile(r"<!-- BEGIN ENV VARS -->\n.*?\n<!-- END ENV VARS -->", re.DOTALL)

    if not pattern.search(readme_text):
        print("❌ Could not find <!-- BEGIN ENV VARS --> markers in README.md")
        return 1

    new_readme_text = pattern.sub(
        f"<!-- BEGIN ENV VARS -->\n{table}\n<!-- END ENV VARS -->", readme_text
    )

    if readme_text != new_readme_text:
        if args.update:
            README.write_text(new_readme_text)
            print("✅ README.md updated with latest environment variables.")
            return 0
        else:
            print("❌ README.md environment variables table is out of date.")
            print("Run `uv run scripts/check_doc_env_vars.py --update` to fix.")
            return 1

    print("✅ README.md environment variables table is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
