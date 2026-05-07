#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that README.md documents all environment variables."""

import argparse
import re
import sys
from pathlib import Path

# Add src directory to sys.path to ensure absolute imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_BEGIN = "<!-- BEGIN ENV VARS -->"
MARKER_END = "<!-- END ENV VARS -->"


def generate_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    # We instantiate to get defaults, but pydantic model_fields also has them
    for field_name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{field_name.upper()}"
        default_val = field_info.default
        if default_val == "" or default_val == []:
            default_str = "empty"
        elif default_val is None:
            default_str = "null"
        else:
            if isinstance(default_val, bool):
                default_str = f"`{'true' if default_val else 'false'}`"
            else:
                default_str = f"`{default_val}`"

        description = field_info.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {description} |")

        # Special case for OpenAI API Key (based on original README)
        if field_name == "openai_api_key":
            lines.append(
                "| `OPENAI_API_KEY` | empty | Alternate OpenAI API key for the LLM wrapper |"
            )

    return "\n".join(lines)


def check_docs() -> int:
    readme_content = README.read_text()
    if MARKER_BEGIN not in readme_content or MARKER_END not in readme_content:
        print("❌ Markers not found in README.md")
        return 1

    table_content = generate_table()

    # Extract current table
    pattern = re.compile(rf"{MARKER_BEGIN}\n(.*?)\n{MARKER_END}", re.DOTALL)
    match = pattern.search(readme_content)
    if not match:
        print("❌ Could not extract current environment variables table")
        return 1

    current_table = match.group(1).strip()
    if current_table != table_content.strip():
        print("❌ Environment variables documentation is out of date.")
        print("Run `uv run scripts/generate_env_docs.py --update` to fix.")
        return 1

    print("✅ Environment variables documentation is up to date.")
    return 0


def update_docs() -> int:
    readme_content = README.read_text()
    if MARKER_BEGIN not in readme_content or MARKER_END not in readme_content:
        print("❌ Markers not found in README.md")
        return 1

    table_content = generate_table()

    pattern = re.compile(rf"({MARKER_BEGIN}\n)(.*?)(\n{MARKER_END})", re.DOTALL)
    new_content = pattern.sub(rf"\1{table_content}\3", readme_content)

    README.write_text(new_content)
    print("✅ Updated environment variables documentation in README.md.")
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if docs are up to date")
    parser.add_argument("--update", action="store_true", help="Update docs")
    args = parser.parse_args()

    if args.update:
        return update_docs()
    elif args.check:
        return check_docs()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
