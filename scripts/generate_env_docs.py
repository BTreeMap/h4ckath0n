#!/usr/bin/env -S uv run python
"""Drift-prevention script to generate README.md environment variables table."""

import argparse
import re
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    from h4ckath0n.config import Settings

    rows = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            var_name = "`OPENAI_API_KEY` or `H4CKATH0N_OPENAI_API_KEY`"
        else:
            var_name = f"`{var_name}`"

        default = field.default if field.default is not None else ""
        if isinstance(default, str) and not default:
            default = "empty"
        elif isinstance(default, bool):
            default = str(default).lower()
        elif isinstance(default, list) and not default:
            default = "[]"

        desc = field.description or ""
        rows.append(f"| {var_name} | `{default}` | {desc} |")

    table_str = "\n".join(rows) + "\n"

    readme_path = Path("README.md")
    readme_content = readme_path.read_text()

    start_marker = "<!-- GENERATED_ENV_VARS_START -->\n"
    end_marker = "<!-- GENERATED_ENV_VARS_END -->"

    pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)

    if not pattern.search(readme_content):
        print("Markers not found in README.md")
        sys.exit(1)

    new_content = pattern.sub(f"{start_marker}{table_str}{end_marker}", readme_content)

    if args.check:
        if new_content != readme_content:
            print("❌ README.md environment variables table is out of date.")
            print("Run `uv run scripts/generate_env_docs.py` to update it.")
            sys.exit(1)
        print("✅ README.md environment variables table is up to date.")
    else:
        readme_path.write_text(new_content)
        print("✅ README.md updated successfully.")


if __name__ == "__main__":
    main()
