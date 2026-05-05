#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify and update environment variable documentation in README.md.

Usage (from repo root):
    uv run scripts/generate_env_docs.py --check
    uv run scripts/generate_env_docs.py --update
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Insert src into sys.path to allow importing h4ckath0n
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def generate_markdown_table() -> str:
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"
        default = field.default

        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"
        elif default == "":
            default_str = "empty"
        elif default == []:
            default_str = "`[]`"
        elif isinstance(default, bool):
            default_str = f"`{str(default).lower()}`"
        else:
            default_str = f"`{default}`"

        desc = field.description or ""

        if name == "openai_api_key":
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
            lines.append(
                f"| `{env_name}` | empty | Alternate OpenAI API key for the LLM wrapper |"
            )
            continue

        lines.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def update_readme(new_table: str, check_only: bool = False) -> bool:
    content = README.read_text()

    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print("❌ Error: Could not find env var markers in README.md")
        return False

    end_idx += len(END_MARKER)

    new_section = f"{START_MARKER}\n{new_table}\n{END_MARKER}"

    old_section = content[start_idx:end_idx]
    if old_section == new_section:
        print("✅ Environment variables documentation is up to date.")
        return True

    if check_only:
        print("❌ Environment variables documentation is out of date.")
        print("Run `uv run scripts/generate_env_docs.py --update` to fix.")
        return False

    new_content = content[:start_idx] + new_section + content[end_idx:]
    README.write_text(new_content)
    print("✅ Environment variables documentation updated in README.md.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate environment variable documentation.")
    parser.add_argument("--check", action="store_true", help="Check if docs are up to date")
    parser.add_argument("--update", action="store_true", help="Update docs in place")
    args = parser.parse_args()

    if not args.check and not args.update:
        parser.print_help()
        return 1

    table = generate_markdown_table()
    success = update_readme(table, check_only=args.check)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
