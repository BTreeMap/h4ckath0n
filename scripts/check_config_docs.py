#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that config documentation in README matches Settings."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pydantic_core import PydanticUndefined

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_settings_table() -> str:
    from h4ckath0n.config import Settings  # noqa: E402

    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            env_name = "OPENAI_API_KEY / H4CKATH0N_OPENAI_API_KEY"

        default_val = getattr(field, "default_factory", None)
        default_val = field.default if default_val is None else default_val()

        if default_val is PydanticUndefined:
            default_val = "Required"

        if default_val == "":
            default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{str(default_val).lower()}`"
        elif isinstance(default_val, list) and len(default_val) == 0:
            default_str = "`[]`"
        else:
            default_str = f"`{default_val}`"

        desc = field.description or ""
        lines.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update the README.md file")
    args = parser.parse_args()

    table = get_settings_table()
    readme_text = README.read_text()

    start_marker = "<!-- CONFIG_START -->"
    end_marker = "<!-- CONFIG_END -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Markers not found in README.md")
        return 1

    start_idx = readme_text.index(start_marker) + len(start_marker)
    end_idx = readme_text.index(end_marker)

    new_readme = readme_text[:start_idx] + "\n" + table + "\n" + readme_text[end_idx:]

    if args.update:
        README.write_text(new_readme)
        print("✅ README.md updated with config documentation.")
        return 0
    else:
        if new_readme != readme_text:
            print("❌ Configuration documentation in README.md is out of date.")
            print("Run `uv run scripts/check_config_docs.py --update` to fix.")
            return 1
        print("✅ Configuration documentation in README.md is up to date.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
