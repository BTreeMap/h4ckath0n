#!/usr/bin/env -S uv run python
"""Drift-prevention script: generate configuration docs from Settings."""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_markdown_table() -> str:
    from pydantic_core import PydanticUndefined

    from h4ckath0n.config import Settings

    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            env_var = "`OPENAI_API_KEY` or `H4CKATH0N_OPENAI_API_KEY`"
        else:
            env_var = f"`H4CKATH0N_{name.upper()}`"

        default_val = field.default
        if default_val is None or default_val == "":
            default_str = "empty"
        elif default_val is PydanticUndefined:
            default_factory = getattr(field, "default_factory", None)
            default_str = f"`{default_factory()}`" if default_factory is not None else "required"
        else:
            # Format booleans as lowercase string `true` / `false` or list as `[]` etc.
            if isinstance(default_val, bool):
                default_str = f"`{str(default_val).lower()}`"
            else:
                default_str = f"`{default_val}`"

        description = field.description or ""

        lines.append(f"| {env_var} | {default_str} | {description} |")

    return "\n".join(lines)


def update_readme(table_content: str) -> bool:
    content = README.read_text()

    start_marker = "<!-- CONFIG_START -->"
    end_marker = "<!-- CONFIG_END -->"

    pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)

    if not pattern.search(content):
        print("❌ Could not find configuration markers in README.md.", file=sys.stderr)
        sys.exit(1)

    new_block = f"{start_marker}\n{table_content}\n{end_marker}"
    new_content = pattern.sub(new_block, content)

    if content == new_content:
        return False

    README.write_text(new_content)
    return True


if __name__ == "__main__":
    table = generate_markdown_table()
    changed = update_readme(table)
    if changed:
        print("✅ README.md configuration table updated.")
    else:
        print("✅ README.md configuration table is already up to date.")
