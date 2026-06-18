#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that README.md documents all config settings.

Usage:
    uv run scripts/check_doc_env.py [--update]
"""

import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_START -->"
END_MARKER = "<!-- CONFIG_END -->"


def get_default_str(default: Any) -> str:
    if default == "":
        return "empty"
    if default is False:
        return "`false`"
    if default is True:
        return "`true`"
    if default == []:
        return "`[]`"
    return f"`{default}`"


def generate_table() -> str:
    from h4ckath0n.config import Settings

    lines = []
    lines.append("| Variable | Default | Description |")
    lines.append("|---|---|---|")

    for name, field_info in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"
        default_str = get_default_str(field_info.default)
        desc = field_info.description or ""

        if name == "openai_api_key":
            lines.append(f"| `OPENAI_API_KEY` | {default_str} | {desc} |")
            lines.append(
                f"| `H4CKATH0N_OPENAI_API_KEY` | {default_str} "
                "| Alternate OpenAI API key for the LLM wrapper |"
            )
        else:
            lines.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    update_mode = "--update" in sys.argv

    table_content = generate_table()
    expected_block = f"{START_MARKER}\n{table_content}\n{END_MARKER}"

    readme_content = README.read_text()

    start_idx = readme_content.find(START_MARKER)
    end_idx = readme_content.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print("❌ Could not find CONFIG_START and CONFIG_END markers in README.md")
        return 1

    current_block = readme_content[start_idx : end_idx + len(END_MARKER)]

    if current_block == expected_block:
        print("✅ README.md config table is up to date.")
        return 0

    if update_mode:
        new_content = (
            readme_content[:start_idx]
            + expected_block
            + readme_content[end_idx + len(END_MARKER) :]
        )
        README.write_text(new_content)
        print("✅ Updated README.md config table.")
        return 0
    else:
        print("❌ README.md config table is out of sync. Run with --update to fix.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
