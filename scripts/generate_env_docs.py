#!/usr/bin/env -S uv run python
"""Drift-prevention script: generate environment variable documentation.

Usage (from repo root):
    uv run scripts/generate_env_docs.py [--check]

The script imports the h4ckath0n app settings, enumerates all fields, and
updates the Configuration table in README.md. If --check is passed, it fails
if the README is out of date.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_env_vars() -> list[tuple[str, str, str]]:
    """Return all environment variables as (name, default, description)."""
    from h4ckath0n.config import Settings

    prefix = Settings.model_config.get("env_prefix", "H4CKATH0N_")

    rows = []
    for field_name, field in Settings.model_fields.items():
        var_name = f"{prefix}{field_name}".upper()

        # Handle default value formatting
        default_val = field.default
        if default_val == "" or default_val is None:
            default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{'true' if default_val else 'false'}`"
        elif isinstance(default_val, (list, str)):
            default_str = f"`{default_val}`"
        else:
            default_str = f"`{default_val}`"

        desc = field.description or ""

        if field_name == "openai_api_key":
            rows.append(("OPENAI_API_KEY", "empty", "OpenAI API key for the LLM wrapper"))
            desc = "Alternate OpenAI API key for the LLM wrapper"

        rows.append((var_name, default_str, desc))

    return rows


def generate_markdown_table(rows: list[tuple[str, str, str]]) -> str:
    """Generate the markdown table string."""
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, default, desc in rows:
        lines.append(f"| `{name}` | {default} | {desc} |")
    return "\n".join(lines)


def update_readme(new_table: str, check_only: bool = False) -> int:
    """Update README.md with the new table or check if it matches."""
    text = README.read_text()

    pattern = re.compile(
        r"(<!-- GENERATED_ENV_VARS_START -->\n)(.*?)(\n<!-- GENERATED_ENV_VARS_END -->)", re.DOTALL
    )

    match = pattern.search(text)
    if not match:
        print("❌ Could not find GENERATED_ENV_VARS markers in README.md")
        return 1

    current_table = match.group(2)

    if current_table == new_table:
        print("✅ README.md environment variables are up to date.")
        return 0

    if check_only:
        print(
            "❌ README.md environment variables are out of date. "
            "Run 'uv run scripts/generate_env_docs.py' to update."
        )
        return 1

    new_text = pattern.sub(rf"\g<1>{new_table}\g<3>", text)
    README.write_text(new_text)
    print("✅ Updated README.md environment variables.")
    return 0


def main() -> int:
    check_only = "--check" in sys.argv
    rows = get_env_vars()
    table = generate_markdown_table(rows)
    return update_readme(table, check_only)


if __name__ == "__main__":
    sys.exit(main())
