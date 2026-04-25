#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all configuration settings are documented in README.md.

Usage (from repo root):
    uv run scripts/generate_env_docs.py [--check]

If --check is provided, fails if the README.md does not match the generated documentation.
Otherwise, updates the README.md in-place.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import json
import re

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_START = "<!-- GENERATED_ENV_VARS_START -->"
MARKER_END = "<!-- GENERATED_ENV_VARS_END -->"

def generate_table() -> str:
    from h4ckath0n.config import Settings

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|"
    ]

    settings_schema = Settings.model_json_schema()
    properties = settings_schema.get("properties", {})

    for name, field_info in properties.items():
        env_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            env_name = "OPENAI_API_KEY / H4CKATH0N_OPENAI_API_KEY"

        default_val = field_info.get("default")
        if default_val is None:
            default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = "`true`" if default_val else "`false`"
        elif isinstance(default_val, list):
            default_str = "`[]`" if not default_val else f"`{json.dumps(default_val)}`"
        else:
            default_str = f"`{default_val}`"

        description = field_info.get("description", "")
        lines.append(f"| `{env_name}` | {default_str} | {description} |")

    return "\n".join(lines)

def update_readme(check_only: bool = False) -> int:
    readme_text = README.read_text()

    # Check if the markers exist
    if MARKER_START not in readme_text or MARKER_END not in readme_text:
        # If not, let's insert them around the table in the configuration section
        config_pattern = re.compile(r"(## Configuration\n\nAll settings use the `H4CKATH0N_` prefix unless noted\.\n\n)(\| Variable \| Default \| Description \|\n\|---\|---\|---\|.*?)(?=\n\n|$)", re.DOTALL)

        match = config_pattern.search(readme_text)
        if match:
            new_text = readme_text[:match.start(2)] + MARKER_START + "\n" + match.group(2) + "\n" + MARKER_END + readme_text[match.end(2):]
            if not check_only:
                README.write_text(new_text)
                readme_text = new_text
            else:
                print("❌ README.md is missing the generated env var markers.")
                return 1
        else:
            print("❌ Could not find the Configuration section in README.md.")
            return 1

    # Generate the new table
    new_table = generate_table()

    # Replace the text between markers
    pattern = re.compile(rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}", re.DOTALL)
    replacement = f"{MARKER_START}\n{new_table}\n{MARKER_END}"

    new_readme_text = pattern.sub(replacement, readme_text)

    if new_readme_text != readme_text:
        if check_only:
            print("❌ The environment variables in README.md are out of date.")
            print("Run `uv run scripts/generate_env_docs.py` to update them.")
            return 1
        else:
            README.write_text(new_readme_text)
            print("✅ Updated environment variables in README.md.")
            return 0
    else:
        print("✅ Environment variables in README.md are up to date.")
        return 0

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if the README.md is up to date")
    args = parser.parse_args()

    return update_readme(check_only=args.check)

if __name__ == "__main__":
    sys.exit(main())
