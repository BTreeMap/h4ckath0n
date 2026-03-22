#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the configuration table in README.md matches the config.

Usage (from repo root):
    uv run scripts/generate_doc_config.py [--check]

The script loads the Settings class from h4ckath0n.config and generates a Markdown table
documenting the settings and their defaults. It injects this table between markers in README.md.
If --check is provided, it fails if the file would be modified.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic.fields import FieldInfo

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
from h4ckath0n.config import Settings  # noqa: E402

README_PATH = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_TABLE_START -->"
END_MARKER = "<!-- CONFIG_TABLE_END -->"


def format_default(name: str, field: FieldInfo) -> str:
    if name == "rp_id":
        return "`localhost` in development"
    if name == "origin":
        return "`http://localhost:8000` in development"
    if name == "openai_api_key":
        return "empty"

    if field.default == "":
        return "empty"
    if field.default == [] or field.default_factory is list:
        return "`[]`"
    if isinstance(field.default, bool):
        return f"`{str(field.default).lower()}`"
    return f"`{field.default}`"


def generate_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        if name in ("openai_api_key",):
            var_name = "OPENAI_API_KEY"

        default_val = format_default(name, field)
        description = field.description or "TODO"
        lines.append(f"| `{var_name}` | {default_val} | {description} |")

        if name == "openai_api_key":
            lines.append(
                f"| `H4CKATH0N_{name.upper()}` | {default_val} | "
                "Alternate OpenAI API key for the LLM wrapper |"
            )
    return "\n".join(lines)


def main() -> int:
    check_only = "--check" in sys.argv
    new_table = generate_table()

    content = README_PATH.read_text(encoding="utf-8")

    if START_MARKER not in content or END_MARKER not in content:
        print(f"Error: Markers {START_MARKER} and {END_MARKER} not found in README.md.")
        return 1

    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER) + len(END_MARKER)

    before = content[:start_idx]
    after = content[end_idx:]

    new_content = f"{before}{START_MARKER}\n{new_table}\n{END_MARKER}{after}"

    if content == new_content:
        print("✅ Configuration table in README.md is up to date.")
        return 0

    if check_only:
        print("❌ Configuration table in README.md is out of date.")
        print("Run 'uv run scripts/generate_doc_config.py' to update it.")
        return 1

    README_PATH.write_text(new_content, encoding="utf-8")
    print("✅ Configuration table in README.md updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
