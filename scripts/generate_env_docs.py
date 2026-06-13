#!/usr/bin/env -S uv run python
"""Drift-prevention script to generate environment variable documentation.

This script parses `src/h4ckath0n/config.py` using Pydantic, extracts the fields
and their descriptions, and updates the configuration table in `README.md`
between the marker comments:
<!-- BEGIN ENV VARS -->
<!-- END ENV VARS -->

Usage (from repo root):
    uv run scripts/generate_env_docs.py [--check]
"""

import argparse
import json
import sys
from pathlib import Path

# Add src/ to sys.path so we can import the app modules
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))


from h4ckath0n.config import Settings  # noqa: E402

README = REPO_ROOT / "README.md"
START_MARKER = "<!-- BEGIN ENV VARS -->\n"
END_MARKER = "<!-- END ENV VARS -->\n"


def format_default(val) -> str:
    if val == "":
        return "empty"
    if isinstance(val, bool):
        return f"`{str(val).lower()}`"
    if isinstance(val, list):
        return f"`{json.dumps(val)}`"
    return f"`{val}`"


def build_markdown_table() -> str:
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field in Settings.model_fields.items():
        var_name = f"`H4CKATH0N_{name.upper()}`"

        # Exception for OPENAI_API_KEY
        if name == "openai_api_key":
            # Add OPENAI_API_KEY as an alias first
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
            desc = "Alternate OpenAI API key for the LLM wrapper"
        else:
            desc = field.description or "Configuration variable"

        default_str = format_default(field.default)
        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"

        lines.append(f"| {var_name} | {default_str} | {desc} |")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Generate environment variable docs.")
    parser.add_argument("--check", action="store_true", help="Check if docs are up to date.")
    args = parser.parse_args()

    content = README.read_text()

    if START_MARKER not in content or END_MARKER not in content:
        print("❌ Could not find BEGIN ENV VARS or END ENV VARS markers in README.md")
        return 1

    start_idx = content.find(START_MARKER) + len(START_MARKER)
    end_idx = content.find(END_MARKER)

    new_table = build_markdown_table()

    new_content = content[:start_idx] + new_table + content[end_idx:]

    if args.check:
        if content != new_content:
            print("❌ README.md environment variables are out of date!")
            print("Run `uv run scripts/generate_env_docs.py` to update them.")
            return 1
        print("✅ README.md environment variables are up to date.")
        return 0
    else:
        README.write_text(new_content)
        print("✅ Updated environment variable docs in README.md")
        return 0


if __name__ == "__main__":
    sys.exit(main())
