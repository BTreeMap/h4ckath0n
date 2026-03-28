#!/usr/bin/env -S uv run python
"""Drift-prevention script: generates markdown configuration table from Settings class.

Usage (from repo root):
    uv run scripts/generate_doc_config.py
    uv run scripts/generate_doc_config.py --check
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_config_table() -> str:
    """Generate a Markdown table of configuration options."""
    from h4ckath0n.config import Settings  # noqa: E402

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field in Settings.model_fields.items():
        if name == "model_config":
            continue

        env_name = f"`H4CKATH0N_{name.upper()}`"

        # Override specific cases based on README.md
        if name == "openai_api_key":
            env_name = "`OPENAI_API_KEY`"

        default_val = field.default
        default_str = ""

        # Safe check for undefined default
        if (
            getattr(type(default_val), "__name__", "") == "PydanticUndefinedType"
            or default_val == ""
            or default_val is None
        ):
            default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{str(default_val).lower()}`"
        elif isinstance(default_val, (int, str)):
            default_str = f"`{default_val}`"
        elif isinstance(default_val, list) and not default_val:
            default_str = "`[]`"
        else:
            default_str = f"`{default_val}`"

        # Hardcode the specific dev defaults as mentioned in the original README
        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"

        desc = field.description or ""
        lines.append(f"| {env_name} | {default_str} | {desc} |")

        if name == "openai_api_key":
            lines.append(
                "| `H4CKATH0N_OPENAI_API_KEY` | empty | "
                "Alternate OpenAI API key for the LLM wrapper |"
            )

    return "\n".join(lines)


def update_readme(check_only: bool = False) -> int:
    """Update or check the README.md configuration table."""
    readme_text = README.read_text()
    table = get_config_table()

    # The marker is exactly `<!-- CONFIG_TABLE_START -->` then newline,
    # then table, then newline `<!-- CONFIG_TABLE_END -->`
    pattern = re.compile(r"<!-- CONFIG_TABLE_START -->.*?<!-- CONFIG_TABLE_END -->", re.DOTALL)
    replacement = f"<!-- CONFIG_TABLE_START -->\n{table}\n<!-- CONFIG_TABLE_END -->"

    if not pattern.search(readme_text):
        print(
            "❌ Marker tags <!-- CONFIG_TABLE_START --> and <!-- CONFIG_TABLE_END --> "
            "not found in README.md"
        )
        return 1

    new_text = pattern.sub(replacement, readme_text)

    if new_text == readme_text:
        print("✅ Configuration table is up to date.")
        return 0

    if check_only:
        print(
            "❌ Configuration table is out of date. "
            "Run `uv run scripts/generate_doc_config.py` to update."
        )
        return 1

    README.write_text(new_text)
    print("✅ Configuration table updated.")
    return 0


def main() -> int:
    check_only = "--check" in sys.argv
    return update_readme(check_only)


if __name__ == "__main__":
    sys.exit(main())
