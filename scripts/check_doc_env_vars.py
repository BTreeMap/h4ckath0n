#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables are documented in README.md.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py [--update]

The script loads the `Settings` model from `h4ckath0n.config` and verifies that
the markdown table within the `<!-- BEGIN ENV VARS -->` and `<!-- END ENV VARS -->`
markers in README.md perfectly matches the generated table.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

BEGIN_MARKER = "<!-- BEGIN ENV VARS -->\n"
END_MARKER = "<!-- END ENV VARS -->\n"


def get_env_vars_table() -> str:
    """Generate a markdown table of environment variables from Settings."""
    from h4ckath0n.config import Settings  # noqa: E402

    rows = []
    rows.append("| Variable | Default | Description |")
    rows.append("|---|---|---|")

    for name, field in Settings.model_fields.items():
        env_var_name = f"H4CKATH0N_{name.upper()}"

        # Determine default value
        if field.is_required():
            default_val = "required"
        elif field.default_factory is not None:
            # Handle list default factory (e.g. bootstrap_admin_emails)
            default_val = "`[]`"
        elif field.default == "" or field.default is None:
            default_val = "empty"
        elif isinstance(field.default, bool):
            default_val = f"`{str(field.default).lower()}`"
        else:
            default_val = f"`{field.default}`"

        # Hardcode specific defaults for consistency with old docs
        if name == "rp_id":
            default_val = "`localhost` in development"
        elif name == "origin":
            default_val = "`http://localhost:8000` in development"

        desc = field.description or ""

        # Custom logic for openai_api_key fallback
        if name == "openai_api_key":
            rows.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
            desc = "Alternate OpenAI API key for the LLM wrapper"

        rows.append(f"| `{env_var_name}` | {default_val} | {desc} |")

    return "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update README.md in place.")
    args = parser.parse_args()

    readme_text = README.read_text()

    if BEGIN_MARKER not in readme_text or END_MARKER not in readme_text:
        print(
            "❌ Markers not found in README.md. "
            "Please add <!-- BEGIN ENV VARS --> and <!-- END ENV VARS -->."
        )
        return 1

    start_idx = readme_text.find(BEGIN_MARKER) + len(BEGIN_MARKER)
    end_idx = readme_text.find(END_MARKER)

    current_table = readme_text[start_idx:end_idx]
    expected_table = get_env_vars_table()

    if current_table == expected_table:
        print("✅ Environment variables table in README.md is up to date.")
        return 0

    if args.update:
        new_readme_text = readme_text[:start_idx] + expected_table + readme_text[end_idx:]
        README.write_text(new_readme_text)
        print("✅ Updated README.md with latest environment variables.")
        return 0
    else:
        print("❌ Environment variables table in README.md is out of date.")
        print("Run `uv run scripts/check_doc_env_vars.py --update` to fix.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
