#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every config variable is documented and generated.

Usage (from repo root):
    uv run scripts/check_doc_config.py [--fix]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

from pydantic_core import PydanticUndefined

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings() -> dict[str, Any]:
    from h4ckath0n.config import Settings

    return Settings.model_fields


def generate_table() -> str:
    from pydantic.fields import FieldInfo

    fields: dict[str, FieldInfo] = get_settings()

    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in fields.items():
        if name == "openai_api_key":
            env_var = "`OPENAI_API_KEY` or `H4CKATH0N_OPENAI_API_KEY`"
        else:
            env_var = f"`H4CKATH0N_{name.upper()}`"

        default_val = field.default
        if default_val == "":
            default_str = "empty"
        elif (
            default_val == []
            or default_val is PydanticUndefined
            and getattr(field, "default_factory", None) is list
        ):
            default_str = "`[]`"
        elif default_val is True:
            default_str = "`true`"
        elif default_val is False:
            default_str = "`false`"
        elif isinstance(default_val, (int, float, str)):
            default_str = f"`{default_val}`"
        else:
            default_str = str(default_val)

        desc = field.description or ""
        lines.append(f"| {env_var} | {default_str} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    do_fix = "--fix" in sys.argv
    readme_text = README.read_text()

    pattern = re.compile(r"(<!-- CONFIG_DOCS_START -->\n).*?(<!-- CONFIG_DOCS_END -->)", re.DOTALL)

    if not pattern.search(readme_text):
        print("❌ Could not find <!-- CONFIG_DOCS_START --> and <!-- CONFIG_DOCS_END --> markers")
        return 1

    expected_table = generate_table()

    new_text = pattern.sub(rf"\g<1>{expected_table}\n\g<2>", readme_text)

    if new_text != readme_text:
        if do_fix:
            README.write_text(new_text)
            print("✅ Updated README.md with generated configuration table.")
            return 0
        else:
            print("❌ Configuration table in README.md is out of date.")
            print("Run `uv run scripts/check_doc_config.py --fix` to update it.")
            return 1

    print("✅ Configuration table in README.md is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
