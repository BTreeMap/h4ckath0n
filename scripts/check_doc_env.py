#!/usr/bin/env -S uv run python
"""Verify and auto-generate environment variable documentation from Settings.

Usage (from repo root):
    uv run scripts/check_doc_env.py [--sync]

With --sync, it will update README.md and .env.example with the latest settings.
Without --sync, it fails if the files are out of sync.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
ENV_EXAMPLE = REPO_ROOT / ".env.example"

# Regex to find the block between markers in README
MARKER_START = "<!-- START ENV DOCS -->"
MARKER_END = "<!-- END ENV DOCS -->"
BLOCK_RE = re.compile(rf"{MARKER_START}.*?{MARKER_END}", re.DOTALL)


def generate_docs() -> tuple[str, str]:
    """Generate the markdown table and .env.example content from Settings."""
    from h4ckath0n.config import Settings

    table_lines = [
        MARKER_START,
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    env_lines = [
        "# Auto-generated from h4ckath0n.config.Settings",
        "# Copy to .env and modify as needed",
        "",
    ]

    for name, field in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"

        # Pydantic v2 compat for default values
        default = field.default
        if (
            default is None or str(default) == "PydanticUndefined"
        ) and field.default_factory is not None:
            default = field.default_factory()

        desc = field.description or ""

        # Format default for Markdown table
        if default == "":
            table_default = "empty"
        elif default is False:
            table_default = "`false`"
        elif default is True:
            table_default = "`true`"
        elif default == []:
            table_default = "`[]`"
        else:
            table_default = f"`{default}`"

        table_lines.append(f"| `{env_name}` | {table_default} | {desc} |")

        # Format for .env.example
        env_lines.append(f"# {desc}")
        if default == "":
            env_lines.append(f"# {env_name}=")
        elif default == []:
            env_lines.append(f"{env_name}=[]")
        elif isinstance(default, bool):
            env_lines.append(f"{env_name}={str(default).lower()}")
        else:
            env_lines.append(f"{env_name}={default}")
        env_lines.append("")

    table_lines.append(MARKER_END)

    return "\n".join(table_lines), "\n".join(env_lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or sync env docs.")
    parser.add_argument("--sync", action="store_true", help="Update docs in place")
    args = parser.parse_args()

    table_content, env_content = generate_docs()

    readme_text = README.read_text()
    if MARKER_START not in readme_text:
        print(f"Error: {MARKER_START} not found in README.md", file=sys.stderr)
        return 1

    new_readme_text = BLOCK_RE.sub(table_content, readme_text)

    current_env = ENV_EXAMPLE.read_text() if ENV_EXAMPLE.exists() else ""

    drift = False

    if new_readme_text != readme_text:
        drift = True
        print("❌ README.md environment docs are out of date.")

    if current_env != env_content:
        drift = True
        print("❌ .env.example is out of date.")

    if args.sync:
        if new_readme_text != readme_text:
            README.write_text(new_readme_text)
            print("✅ Synced README.md")
        if current_env != env_content:
            ENV_EXAMPLE.write_text(env_content)
            print("✅ Synced .env.example")
        return 0

    if drift:
        print("\nRun `uv run scripts/check_doc_env.py --sync` to fix.")
        return 1

    print("✅ Environment documentation is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
