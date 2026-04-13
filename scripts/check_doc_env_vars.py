#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables are documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py [--update]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- BEGIN ENV VARS -->\n"
END_MARKER = "<!-- END ENV VARS -->\n"


def get_env_var_table() -> str:
    """Generate markdown table from Settings model."""
    from h4ckath0n.config import Settings

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"

        default = field.default
        if default == "":
            default_str = "empty"
        elif default is False:
            default_str = "`false`"
        elif default is True:
            default_str = "`true`"
        elif default == []:
            default_str = "`[]`"
        else:
            default_str = f"`{default}`"

        desc = field.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {desc} |")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    table = get_env_var_table()

    readme_text = README.read_text()

    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        print("❌ Markers not found in README.md")
        return 1

    start_idx = readme_text.index(START_MARKER) + len(START_MARKER)
    end_idx = readme_text.index(END_MARKER)

    current_table = readme_text[start_idx:end_idx]

    if current_table == table:
        print("✅ Environment variables documentation is up to date.")
        return 0

    if args.update:
        new_text = readme_text[:start_idx] + table + readme_text[end_idx:]
        README.write_text(new_text)
        print("✅ Updated environment variables documentation in README.md.")
        return 0

    print("❌ Environment variables documentation is out of date. Run with --update to fix.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
