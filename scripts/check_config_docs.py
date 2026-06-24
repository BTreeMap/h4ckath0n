#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that config env vars are documented.

Usage (from repo root):
    uv run scripts/check_config_docs.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pydantic_core

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_expected_table() -> str:
    from h4ckath0n.config import Settings  # noqa: E402

    fields = Settings.model_fields
    rows = []

    rows.append("| Variable | Default | Description |")
    rows.append("|---|---|---|")

    for name, field in fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"

        if name == "openai_api_key":
            rows.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
            rows.append(
                "| `H4CKATH0N_OPENAI_API_KEY` | empty "
                "| Alternate OpenAI API key for the LLM wrapper |"
            )
            continue

        default: Any = field.default
        if default is pydantic_core.PydanticUndefined:
            default = getattr(field, "default_factory", None)
            default = default() if default else "empty"

        if default == "":
            default_str = "empty"
        elif default == []:
            default_str = "`[]`"
        elif isinstance(default, bool):
            default_str = f"`{str(default).lower()}`"
        elif isinstance(default, str) and default != "empty":
            default_str = f"`{default}`"
        else:
            default_str = f"`{default}`"

        desc = field.description or "TODO: add description in config.py"
        rows.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(rows)


def main() -> int:
    expected_table = get_expected_table()
    readme_text = README.read_text()

    start_marker = "<!-- CONFIG_START -->"
    end_marker = "<!-- CONFIG_END -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Markers not found in README.md")
        return 1

    start_idx = readme_text.find(start_marker) + len(start_marker)
    end_idx = readme_text.find(end_marker)

    actual_table = readme_text[start_idx:end_idx].strip()

    if actual_table != expected_table:
        print("❌ Configuration documentation in README.md is out of sync.")
        print("Expected:\n" + expected_table)
        print("\nActual:\n" + actual_table)
        print("\nUpdate README.md to match the expected table.")
        return 1

    print("✅ Configuration documentation is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
