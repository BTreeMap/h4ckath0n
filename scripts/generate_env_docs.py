#!/usr/bin/env python
"""Generate environment variable documentation from the Settings model."""

import argparse
import sys
from pathlib import Path
from typing import Any

from pydantic_core import PydanticUndefined

# Important to add src to sys.path so we can import h4ckath0n in a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from h4ckath0n.config import Settings

README_PATH = Path("README.md")
START_MARKER = "<!-- GENERATED_ENV_VARS_START -->\n"
END_MARKER = "<!-- GENERATED_ENV_VARS_END -->\n"


def format_default(default: Any) -> str:
    if default == "":
        return "empty"
    if default is PydanticUndefined:
        return "required"
    if isinstance(default, bool):
        return "`true`" if default else "`false`"
    if isinstance(default, list):
        return f"`{default}`"
    return f"`{default}`"


def generate_table() -> str:
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    # Access the model_fields attribute from the model class
    for field_name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{field_name.upper()}"
        default_val = field_info.default
        default_str = format_default(default_val)
        desc = field_info.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {desc} |")
    return "\n".join(lines) + "\n"


def update_readme(check: bool = False) -> int:
    readme_content = README_PATH.read_text(encoding="utf-8")

    if START_MARKER not in readme_content or END_MARKER not in readme_content:
        print(f"Error: {START_MARKER.strip()} or {END_MARKER.strip()} not found in README.md")
        return 1

    start_idx = readme_content.find(START_MARKER) + len(START_MARKER)
    end_idx = readme_content.find(END_MARKER)

    before = readme_content[:start_idx]
    after = readme_content[end_idx:]

    new_table = generate_table()
    new_content = before + new_table + after

    if check:
        if new_content != readme_content:
            print("❌ README.md environment variables are out of date.")
            print("Run `uv run scripts/generate_env_docs.py` to update.")
            return 1
        print("✅ README.md environment variables are up to date.")
        return 0
    else:
        README_PATH.write_text(new_content, encoding="utf-8")
        print("✅ README.md environment variables updated.")
        return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="Check if README.md is up to date without modifying"
    )
    args = parser.parse_args()
    sys.exit(update_readme(check=args.check))


if __name__ == "__main__":
    main()
