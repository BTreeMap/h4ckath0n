#!/usr/bin/env -S uv run python
"""Drift-prevention check and generator: ensure that all configuration settings in Settings
are documented in README.md.

Usage (from repo root):
    uv run scripts/generate_env_docs.py          # Regenerates the table in README.md
    uv run scripts/generate_env_docs.py --check  # Fails if README.md is out of date
"""

import argparse
import sys
from pathlib import Path
from typing import Any

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_START = "<!-- GENERATED_ENV_VARS_START -->\n"
MARKER_END = "<!-- GENERATED_ENV_VARS_END -->\n"


def format_default(val: Any) -> str:
    """Format default value for markdown table."""
    if val == "":
        return "empty"
    if val is None:
        return "empty"
    if isinstance(val, bool):
        return str(val).lower()
    if isinstance(val, list) and not val:
        return "`[]`"
    return f"`{val}`"


def generate_table() -> str:
    """Generate the markdown table of environment variables."""
    env_prefix = Settings.model_config.get("env_prefix", "")

    lines = ["| Variable | Default | Description |\n", "|---|---|---|\n"]

    for name, field in Settings.model_fields.items():
        var_name = f"`{env_prefix}{name}`".upper()
        default_val = format_default(field.default)

        # Look for custom formatting for known fields based on the previous README
        if name == "rp_id":
            default_val = "`localhost` in development"
        elif name == "origin":
            default_val = "`http://localhost:8000` in development"

        desc = field.description or ""

        lines.append(f"| {var_name} | {default_val} | {desc} |\n")

        # Also add OPENAI_API_KEY without prefix if we see openai_api_key
        if name == "openai_api_key":
            lines.append(f"| `OPENAI_API_KEY` | {default_val} | {desc} (alias) |\n")

    return "".join(lines)


def update_readme(content: str, dry_run: bool = False) -> bool:
    """Update README.md with the new table. Returns True if changed."""
    readme_text = README.read_text()

    if MARKER_START not in readme_text or MARKER_END not in readme_text:
        print(
            f"❌ Could not find markers {MARKER_START.strip()} and "
            f"{MARKER_END.strip()} in README.md"
        )
        sys.exit(1)

    start_idx = readme_text.find(MARKER_START) + len(MARKER_START)
    end_idx = readme_text.find(MARKER_END)

    new_text = readme_text[:start_idx] + content + readme_text[end_idx:]

    if new_text == readme_text:
        return False

    if not dry_run:
        README.write_text(new_text)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if out of date")
    args = parser.parse_args()

    table_content = generate_table()

    changed = update_readme(table_content, dry_run=args.check)

    if args.check:
        if changed:
            print(
                "❌ README.md is out of date. "
                "Run `uv run scripts/generate_env_docs.py` to update it."
            )
            return 1
        print("✅ README.md environment variables are up to date.")
        return 0

    if changed:
        print("✅ Updated README.md with latest environment variables.")
    else:
        print("✅ README.md environment variables are already up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
