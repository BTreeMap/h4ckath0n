#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables are documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py [--update]
"""

import argparse
import re
import sys
from pathlib import Path


def get_settings_table() -> str:
    from h4ckath0n.config import Settings

    rows = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            rows.append(f"| `OPENAI_API_KEY` | empty | {field.description or ''} |")

        default_val = (
            "empty"
            if field.default == ""
            else (
                "[]"
                if getattr(field, "default_factory", None)
                else str(field.default).lower()
                if isinstance(field.default, bool)
                else str(field.default)
            )
        )

        rows.append(f"| `{var_name}` | `{default_val}` | {field.description or ''} |")

    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    readme_path = repo_root / "README.md"

    readme_text = readme_path.read_text(encoding="utf-8")

    start_marker = "<!-- BEGIN ENV VARS -->"
    end_marker = "<!-- END ENV VARS -->"

    pattern = re.compile(rf"{start_marker}.*?{end_marker}", re.DOTALL)

    if not pattern.search(readme_text):
        print("❌ Could not find ENV VARS markers in README.md")
        return 1

    new_table = get_settings_table()
    replacement = f"{start_marker}\n{new_table}\n{end_marker}"

    if args.update:
        new_text = pattern.sub(replacement, readme_text)
        if new_text != readme_text:
            readme_path.write_text(new_text, encoding="utf-8")
            print("✅ Updated README.md with latest environment variables")
        else:
            print("✅ README.md is already up to date")
        return 0

    current_match = pattern.search(readme_text)
    if current_match and current_match.group(0) != replacement:
        print("❌ Environment variables in README.md are out of sync.")
        print("Run `uv run scripts/check_doc_env_vars.py --update` to fix.")
        return 1

    print("✅ Environment variables in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
