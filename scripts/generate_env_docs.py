#!/usr/bin/env -S uv run python
"""Drift-prevention script: generates markdown table of env vars from Settings."""

import argparse
import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- GENERATED_ENV_VARS_START -->\n"
END_MARKER = "<!-- GENERATED_ENV_VARS_END -->\n"


def generate_markdown_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for field_name, field_info in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{field_name.upper()}"
        if field_name == "env":
            # Special override for 'env' to match existing docs
            lines.append(f"| `{env_name}` | `development` | {field_info.description or ''} |")
            continue
        if field_name == "openai_api_key":
            # Special case for OpenAI API key alias
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")

        default_val = field_info.default
        if (
            default_val is None
            or str(default_val) == ""
            or (isinstance(default_val, list) and not default_val)
        ):
            default_str = "`[]`" if isinstance(default_val, list) else "empty"
        elif str(default_val) == "PydanticUndefined":
            if field_info.default_factory is list:
                default_str = "`[]`"
            elif field_info.default_factory is dict:
                default_str = "`{}`"
            else:
                default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{str(default_val).lower()}`"
        else:
            default_str = f"`{default_val}`"

        # Specific overrides to match current README exactly
        if field_name == "rp_id":
            default_str = "`localhost` in development"
        elif field_name == "origin":
            default_str = "`http://localhost:8000` in development"

        desc = field_info.description or ""
        lines.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(lines) + "\n"


def update_readme(table_content: str, check_only: bool) -> int:
    text = README.read_text(encoding="utf-8")

    start_idx = text.find(START_MARKER)
    end_idx = text.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print("Error: Markers not found in README.md")
        return 1

    before = text[: start_idx + len(START_MARKER)]
    after = text[end_idx:]

    new_text = before + table_content + after

    if check_only:
        if text != new_text:
            print("❌ Environment variable documentation is out of sync!")
            print("Run 'uv run scripts/generate_env_docs.py' to update README.md.")
            return 1
        print("✅ Environment variable documentation is up to date.")
        return 0

    README.write_text(new_text, encoding="utf-8")
    print("✅ README.md updated.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check for drift without writing")
    args = parser.parse_args()

    table = generate_markdown_table()
    return update_readme(table, args.check)


if __name__ == "__main__":
    sys.exit(main())
