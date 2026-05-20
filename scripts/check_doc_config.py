#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the configuration table in README.md is up to date.

Usage (from repo root):
    uv run scripts/check_doc_config.py [--fix]
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_START = "<!-- ENV_VARS_START -->\n"
MARKER_END = "<!-- ENV_VARS_END -->\n"


def generate_config_table() -> str:
    """Generate a Markdown table of environment variables from Settings."""
    from h4ckath0n.config import Settings

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            lines.append(
                f"| `OPENAI_API_KEY` | empty | "
                f"{field.description or 'OpenAI API key for the LLM wrapper'} |"
            )
            lines.append(
                f"| `H4CKATH0N_OPENAI_API_KEY` | empty | "
                f"Alternate {field.description or 'OpenAI API key for the LLM wrapper'} |"
            )
            continue

        env_var = f"H4CKATH0N_{name.upper()}"

        default = field.default
        if str(default) == "PydanticUndefined":
            default_str = "`[]`" if name == "bootstrap_admin_emails" else "empty"
        elif default == "":
            default_str = "empty"
        elif default == []:
            default_str = "`[]`"
        elif isinstance(default, bool):
            default_str = f"`{str(default).lower()}`"
        elif default is None:
            default_str = "empty"
        else:
            default_str = f"`{default}`"

        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"

        desc = field.description or ""

        lines.append(f"| `{env_var}` | {default_str} | {desc} |")

    return "\n".join(lines) + "\n"


def main() -> int:
    fix = "--fix" in sys.argv
    readme_text = README.read_text()

    if MARKER_START not in readme_text or MARKER_END not in readme_text:
        print(
            "❌ Markers not found in README.md. "
            "Please add <!-- ENV_VARS_START --> and <!-- ENV_VARS_END -->."
        )
        return 1

    start_idx = readme_text.index(MARKER_START) + len(MARKER_START)
    end_idx = readme_text.index(MARKER_END)

    current_table = readme_text[start_idx:end_idx]
    expected_table = generate_config_table()

    if current_table == expected_table:
        print("✅ Environment variables documentation is up to date.")
        return 0

    if fix:
        new_text = readme_text[:start_idx] + expected_table + readme_text[end_idx:]
        README.write_text(new_text)
        print("✅ Updated README.md with latest environment variables.")
        return 0
    else:
        print("❌ Environment variables documentation is out of date.")
        print("Run `uv run scripts/check_doc_config.py --fix` to update it.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
