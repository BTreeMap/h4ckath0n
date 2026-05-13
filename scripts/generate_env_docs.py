#!/usr/bin/env -S uv run python
"""Drift-prevention script to generate environment variable documentation from Pydantic models.

Usage:
    uv run scripts/generate_env_docs.py --check
    uv run scripts/generate_env_docs.py --update
"""

import argparse
import sys
from pathlib import Path

# Need to import Settings from src to parse it
from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- BEGIN ENV VARS -->\n"
END_MARKER = "<!-- END ENV VARS -->\n"


def generate_markdown_table() -> str:
    """Generate a Markdown table describing all environment variables."""
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for field_name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{field_name.upper()}"

        # Handle default value representation
        default_val = field_info.default
        if field_name == "rp_id":
            default_str = "`localhost` in development"
        elif field_name == "origin":
            default_str = "`http://localhost:8000` in development"
        elif field_name == "env":
            default_str = "`development`"
        elif field_name == "database_url":
            default_str = "`sqlite:///./h4ckath0n.db`"
        elif default_val == "":
            default_str = "empty"
        elif default_val is False:
            default_str = "`false`"
        elif default_val is True:
            default_str = "`true`"
        elif default_val == []:
            default_str = "`[]`"
        else:
            default_str = f"`{default_val}`"

        desc = field_info.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {desc} |")

    # Add exceptions documented manually
    lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")

    return "\n".join(lines) + "\n"


def read_readme() -> str:
    return README.read_text(encoding="utf-8")


def write_readme(content: str) -> None:
    README.write_text(content, encoding="utf-8")


def update_readme(table_content: str) -> bool:
    content = read_readme()
    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print(
            "Error: Could not find BEGIN ENV VARS or END ENV VARS markers in README.md",
            file=sys.stderr,
        )
        return False

    start_idx += len(START_MARKER)

    new_content = content[:start_idx] + table_content + content[end_idx:]
    if new_content == content:
        return False  # No change needed
    write_readme(new_content)
    return True


def check_readme(table_content: str) -> bool:
    content = read_readme()
    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print(
            "Error: Could not find BEGIN ENV VARS or END ENV VARS markers in README.md",
            file=sys.stderr,
        )
        return False

    start_idx += len(START_MARKER)
    current_table = content[start_idx:end_idx]

    return current_table == table_content


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate/check environment variable documentation."
    )
    parser.add_argument("--check", action="store_true", help="Check if README.md is up to date.")
    parser.add_argument(
        "--update", action="store_true", help="Update README.md with generated documentation."
    )
    args = parser.parse_args()

    if not args.check and not args.update:
        parser.print_help()
        return 1

    table_content = generate_markdown_table()

    if args.update:
        if update_readme(table_content):
            print("✅ README.md updated successfully.")
        else:
            print("✅ README.md is already up to date.")
        return 0

    if args.check:
        if check_readme(table_content):
            print("✅ README.md environment variables documentation is up to date.")
            return 0
        else:
            print("❌ README.md environment variables documentation is out of date.")
            print("Run `uv run scripts/generate_env_docs.py --update` to fix it.")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
