#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all configuration variables are documented.

Usage (from repo root):
    uv run scripts/check_doc_config.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic_core import PydanticUndefined

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_table() -> str:
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            lines.append(f"| `OPENAI_API_KEY` | empty | {field.description or ''} |")
            lines.append(f"| `H4CKATH0N_OPENAI_API_KEY` | empty | {field.description or ''} |")
            continue

        var_name = f"H4CKATH0N_{name.upper()}"
        default = field.default if field.default != "" else "empty"
        if default == PydanticUndefined and field.default_factory is not None:
            default = field.default_factory()

        if isinstance(default, bool):
            default = str(default).lower()
        if isinstance(default, list) and not default:
            default = "[]"

        desc = field.description or ""
        lines.append(f"| `{var_name}` | `{default}` | {desc} |")
    return "\n".join(lines)


def main() -> int:
    readme_text = README.read_text()

    start_marker = "<!-- BEGIN CONFIG TABLE -->"
    end_marker = "<!-- END CONFIG TABLE -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Could not find configuration table markers in README.md.")
        print(f"Ensure the config table is wrapped in {start_marker} and {end_marker}")
        return 1

    start_idx = readme_text.find(start_marker) + len(start_marker)
    end_idx = readme_text.find(end_marker)

    current_table = readme_text[start_idx:end_idx].strip()
    expected_table = generate_table().strip()

    if current_table != expected_table:
        print("❌ Configuration documentation in README.md is out of sync with Settings.")
        print("\nExpected table:")
        print(expected_table)
        print("\nPlease update the README.md to match the generated table.")
        return 1

    print("✅ Configuration variables in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
