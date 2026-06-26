#!/usr/bin/env -S uv run python
"""Generates configuration documentation and injects it into README.md."""

import re
import sys
from pathlib import Path

from pydantic_core import PydanticUndefined

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_table() -> str:
    from h4ckath0n.config import Settings

    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            var_name = "OPENAI_API_KEY / H4CKATH0N_OPENAI_API_KEY"

        default = field.default
        if default is PydanticUndefined:
            default = getattr(field, "default_factory", None)
            if default is not None:
                default = "`[]`" if getattr(default, "__name__", "") == "list" else "factory"
            else:
                default = "required"
        elif default == "":
            default = "empty"
        elif isinstance(default, list) and len(default) == 0:
            default = "`[]`"
        elif isinstance(default, bool):
            default = f"`{str(default).lower()}`"
        elif isinstance(default, (int, str)):
            if default != "empty":
                default = f"`{default}`"

        desc = field.description or ""
        lines.append(f"| `{var_name}` | {default} | {desc} |")

    return "\n".join(lines)


def main():
    table = generate_table()
    readme_text = README.read_text()

    start_marker = "<!-- CONFIG_START -->"
    end_marker = "<!-- CONFIG_END -->"

    pattern = re.compile(rf"{start_marker}.*?{end_marker}", re.DOTALL)

    if start_marker not in readme_text:
        print("Markers not found in README.md")
        return 1

    new_text = pattern.sub(f"{start_marker}\n{table}\n{end_marker}", readme_text)
    README.write_text(new_text)
    print("Updated README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
