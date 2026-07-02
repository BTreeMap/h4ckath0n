#!/usr/bin/env -S uv run python
"""Drift-prevention generator: Update the configuration table in README.md.

Usage (from repo root):
    uv run scripts/generate_config_docs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from pydantic_core import PydanticUndefined

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main() -> int:
    from h4ckath0n.config import Settings

    fields = Settings.model_fields

    table_lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in fields.items():
        if field.default is PydanticUndefined:
            default_val = getattr(field, "default_factory", None)
            default_val = f"`{default_val()}`" if default_val is not None else "required"
        else:
            default_val = f"`{field.default}`"

        # Format defaults to match existing table style
        if default_val == "`[]`":
            default_val = "`[]`"
        elif default_val == "`False`":
            default_val = "`false`"
        elif default_val == "`True`":
            default_val = "`true`"
        elif default_val == "``":
            default_val = "empty"

        env_name = f"H4CKATH0N_{name.upper()}"

        # Use field description if available, otherwise fallback
        desc = field.description or "Configuration option"

        # Handle special cases from existing table
        if name == "openai_api_key":
            table_lines.append(
                f"| `OPENAI_API_KEY` | {default_val} | OpenAI API key for the LLM wrapper |"
            )
            table_lines.append(
                f"| `H4CKATH0N_OPENAI_API_KEY` | {default_val} | Alternate "
                f"OpenAI API key for the LLM wrapper |"
            )
            continue

        table_lines.append(f"| `{env_name}` | {default_val} | {desc} |")

    new_table = "\n".join(table_lines)

    readme_text = README.read_text()

    pattern = re.compile(
        r"(<!-- CONFIG_DOCS_START -->\n).*?(\n<!-- CONFIG_DOCS_END -->)", re.DOTALL
    )

    if not pattern.search(readme_text):
        print("❌ Could not find CONFIG_DOCS_START/END markers in README.md")
        return 1

    new_readme = pattern.sub(rf"\g<1>{new_table}\g<2>", readme_text)

    README.write_text(new_readme)
    print("✅ Configuration table generated in README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
