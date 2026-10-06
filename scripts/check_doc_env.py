#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that README.md environment variables match Settings exactly.

This script ensures the configuration table in the README is automatically generated
from the Pydantic Settings model, preventing drift between the code and docs.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_env_table() -> str:
    from h4ckath0n.config import Settings

    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    # Sort fields if desired, but we'll stick to original order
    for field_name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{field_name.upper()}"
        if var_name == "H4CKATH0N_OPENAI_API_KEY":
            # Add OPENAI_API_KEY explicitly before the H4CKATH0N_ variant as per original README
            lines.append(
                "| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |"
            )

        default = field_info.default
        if default is None or default == "":
            default_str = "empty"
        elif isinstance(default, bool):
            default_str = f"`{str(default).lower()}`"
        elif isinstance(default, list):
            default_str = "`[]`"
        else:
            default_str = f"`{default}`"

        if var_name == "H4CKATH0N_RP_ID":
            default_str = "`localhost` in development"
        elif var_name == "H4CKATH0N_ORIGIN":
            default_str = "`http://localhost:8000` in development"

        description = field_info.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {description} |")

    return "\n".join(lines)


def check_env_docs() -> int:
    readme_text = README.read_text()
    expected_table = generate_env_table()

    # We replace between "## Configuration" and "\n\nIn development"
    # To check if it's identical

    start_marker = "All settings use the `H4CKATH0N_` prefix unless noted.\n\n"
    end_marker = "\n\nIn development, missing `RP_ID`"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Could not find configuration table boundaries in README.md")
        return 1

    start_idx = readme_text.index(start_marker) + len(start_marker)
    end_idx = readme_text.index(end_marker)

    current_table = readme_text[start_idx:end_idx].strip()

    if current_table != expected_table.strip():
        print("❌ README.md environment variables table is out of sync with Settings.")
        print("\nTo fix, run: uv run scripts/generate_env_docs.py")
        return 1

    print("✅ Environment variables documentation matches Settings.")
    return 0


if __name__ == "__main__":
    sys.exit(check_env_docs())
