#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables are documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py [--update]

The script generates a markdown table of environment variables from
src/h4ckath0n/config.py and checks that README.md has exactly this table.
With --update, it overwrites the section between <!-- BEGIN ENV VARS --> and <!-- END ENV VARS -->.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_expected_table() -> str:
    """Generate the expected markdown table from Settings."""
    from h4ckath0n.config import Settings

    prefix = Settings.model_config.get("env_prefix", "")

    rows = []
    rows.append("| Variable | Default | Description |")
    rows.append("|---|---|---|")

    for name, field in Settings.model_fields.items():
        env_name = f"{prefix}{name}".upper()

        # Handle default value representation
        if not field.is_required() and field.default_factory is list:
            default_str = "`[]`"
        else:
            default = field.default
            if default is None or (isinstance(default, str) and default == ""):
                default_str = "empty"
            elif default == []:
                default_str = "`[]`"
            elif isinstance(default, bool):
                default_str = f"`{'true' if default else 'false'}`"
            else:
                default_str = f"`{default}`"

        desc = field.description or ""
        rows.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update the README")
    args = parser.parse_args()

    expected_table = get_expected_table()
    readme_text = README.read_text(encoding="utf-8")

    begin_marker = "<!-- BEGIN ENV VARS -->\n"
    end_marker = "<!-- END ENV VARS -->\n"

    begin_idx = readme_text.find(begin_marker)
    end_idx = readme_text.find(end_marker)

    if begin_idx == -1 or end_idx == -1:
        print(
            "❌ Cannot find <!-- BEGIN ENV VARS --> or <!-- END ENV VARS --> markers in README.md."
        )
        return 1

    current_table = readme_text[begin_idx + len(begin_marker) : end_idx].strip()

    if expected_table == current_table:
        print("✅ Environment variable documentation is up to date.")
        return 0

    if args.update:
        new_text = (
            readme_text[: begin_idx + len(begin_marker)]
            + expected_table
            + "\n"
            + readme_text[end_idx:]
        )
        README.write_text(new_text, encoding="utf-8")
        print("✅ README.md has been updated.")
        return 0
    else:
        print("❌ Environment variable documentation is out of date.\n")
        print("Run with --update to fix this.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
