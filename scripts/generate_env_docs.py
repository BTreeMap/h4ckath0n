#!/usr/bin/env -S uv run python
"""Drift-prevention script to generate environment variable documentation.

This script extracts fields from the Settings class in src/h4ckath0n/config.py
and updates the README.md table with the accurate default values and types.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from pydantic.fields import FieldInfo

# Add src to path to import h4ckath0n
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_START = "<!-- GENERATED_ENV_VARS_START -->"
MARKER_END = "<!-- GENERATED_ENV_VARS_END -->"


def format_default(field: FieldInfo) -> str:
    """Format the default value for markdown."""
    if field.default_factory is not None:
        return "*(computed)*"
    if field.default is ... or field.default is None:
        return ""
    if field.default == "":
        return "*empty*"
    if isinstance(field.default, bool):
        return str(field.default).lower()
    return f"`{field.default}`"


def generate_table() -> str:
    """Generate the markdown table for environment variables."""
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        env_var = (
            "OPENAI_API_KEY` or `H4CKATH0N_OPENAI_API_KEY"
            if name == "openai_api_key"
            else f"H4CKATH0N_{name.upper()}"
        )
        default = format_default(field)
        description = field.description or ""
        lines.append(f"| `{env_var}` | {default} | {description} |")
    return "\n".join(lines)


def update_readme(check_only: bool = False) -> int:
    """Update README.md with the generated table."""
    readme_text = README.read_text()

    # Check if markers exist
    if MARKER_START not in readme_text or MARKER_END not in readme_text:
        print(f"❌ Error: {MARKER_START} and {MARKER_END} not found in README.md", file=sys.stderr)
        return 1

    table = generate_table()

    # Build replacement
    pattern = re.compile(rf"{MARKER_START}.*?{MARKER_END}", re.DOTALL)
    replacement = f"{MARKER_START}\n{table}\n{MARKER_END}"

    new_readme_text = pattern.sub(replacement, readme_text)

    if readme_text == new_readme_text:
        print("✅ Environment variables documentation is up to date.")
        return 0

    if check_only:
        print("❌ Error: Environment variables documentation is out of date.", file=sys.stderr)
        print("Run `uv run scripts/generate_env_docs.py` to update.", file=sys.stderr)
        return 1

    README.write_text(new_readme_text)
    print("✅ Updated environment variables documentation in README.md.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate environment variables documentation.")
    parser.add_argument(
        "--check", action="store_true", help="Check if the documentation is up to date."
    )
    args = parser.parse_args()
    return update_readme(check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
