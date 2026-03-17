#!/usr/bin/env -S uv run python
"""Drift-prevention check: auto-generate the configuration table in README.md.

Usage (from repo root):
    uv run scripts/generate_doc_config.py

The script imports the h4ckath0n app settings and generates a markdown table.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_info() -> list[tuple[str, str, str]]:
    from h4ckath0n.config import Settings

    info = []

    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"

        if name == "openai_api_key":
            default_val = "empty"
        elif field.default == "":
            default_val = "empty"
        elif isinstance(field.default, bool):
            default_val = "`true`" if field.default else "`false`"
        elif isinstance(field.default, list) and not field.default:
            default_val = "`[]`"
        else:
            default_val = f"`{field.default}`"

        desc = field.description or ""
        info.append((var_name, default_val, desc))

    return info


def generate_markdown_table(info: list[tuple[str, str, str]]) -> str:
    lines = [
        "<!-- BEGIN_CONFIG_TABLE -->",
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for var_name, default, desc in info:
        lines.append(f"| `{var_name}` | {default} | {desc} |")

    # Manually add alias for OpenAI key
    lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")

    lines.append("<!-- END_CONFIG_TABLE -->")
    return "\n".join(lines)


def update_readme(table_content: str) -> None:
    readme_text = README.read_text()

    if "<!-- BEGIN_CONFIG_TABLE -->" in readme_text and "<!-- END_CONFIG_TABLE -->" in readme_text:
        pattern = re.compile(
            r"<!-- BEGIN_CONFIG_TABLE -->.*?<!-- END_CONFIG_TABLE -->", re.DOTALL
        )
        new_text = pattern.sub(table_content, readme_text)
        README.write_text(new_text)
        return

    # Find table manually
    lines = readme_text.splitlines()
    start_idx = -1
    end_idx = -1

    for i, line in enumerate(lines):
        if line.startswith("| Variable | Default | Description |"):
            start_idx = i
        elif (
            start_idx != -1
            and i > start_idx
            and not line.startswith("|")
            and end_idx == -1
        ):
            end_idx = i

    if start_idx != -1 and end_idx != -1:
        new_lines = lines[:start_idx] + [table_content] + lines[end_idx:]
        new_text = "\n".join(new_lines)
        README.write_text(new_text)
        print("✅ Successfully updated README.md with generated configuration table.")
    else:
        print("Could not find the configuration table in README.md")
        sys.exit(1)


def main() -> int:
    # Always read table content first to check drift
    info = get_settings_info()
    table = generate_markdown_table(info)

    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        readme_text = README.read_text()

        if "<!-- BEGIN_CONFIG_TABLE -->" not in readme_text:
            print(
                "❌ The configuration table in README.md is not using the generated markers."
            )
            return 1

        pattern = re.compile(
            r"<!-- BEGIN_CONFIG_TABLE -->.*?<!-- END_CONFIG_TABLE -->", re.DOTALL
        )
        match = pattern.search(readme_text)

        if not match:
            print("❌ Markers found but regex failed.")
            return 1

        current_table = match.group(0)

        if current_table.strip() != table.strip():
            print("❌ Configuration table in README.md is out of date.")
            print("Run `uv run scripts/generate_doc_config.py` to update it.")
            return 1

        print("✅ Configuration table is up to date.")
        return 0

    update_readme(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
