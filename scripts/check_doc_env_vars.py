#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables are documented in README.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def _format_default(val: Any) -> str:
    if val == "" or val == []:
        return "empty"
    if isinstance(val, bool):
        return "`true`" if val else "`false`"
    return f"`{val}`"


def generate_env_var_table() -> str:
    from h4ckath0n.config import Settings  # noqa: E402

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        default_str = _format_default(field.default)
        desc = field.description or "No description"
        # Custom overrides for docs based on existing README behavior
        if var_name == "H4CKATH0N_RP_ID":
            default_str = "`localhost` in development"
        if var_name == "H4CKATH0N_ORIGIN":
            default_str = "`http://localhost:8000` in development"

        lines.append(f"| `{var_name}` | {default_str} | {desc} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update the README in-place")
    args = parser.parse_args()

    readme_text = README.read_text()
    marker_begin = "<!-- BEGIN ENV VARS -->"
    marker_end = "<!-- END ENV VARS -->"

    if marker_begin not in readme_text or marker_end not in readme_text:
        print("❌ Markers not found in README.md")
        return 1

    table = generate_env_var_table()
    new_section = f"{marker_begin}\n{table}\n{marker_end}"

    pattern = re.compile(rf"{marker_begin}.*?{marker_end}", re.DOTALL)
    current_section_match = pattern.search(readme_text)
    if not current_section_match:
        print("❌ Could not parse existing section")
        return 1

    if current_section_match.group(0) == new_section:
        print("✅ Environment variables documentation is up to date.")
        return 0

    if args.update:
        new_readme = pattern.sub(new_section, readme_text)
        README.write_text(new_readme)
        print("✅ Updated README.md with latest environment variables.")
        return 0
    else:
        print("❌ Environment variables documentation in README.md is out of date.")
        print("Run 'uv run scripts/check_doc_env_vars.py --update' to fix.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
