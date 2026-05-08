#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify and update environment variable documentation in README.md.

Usage (from repo root):
    uv run scripts/generate_env_docs.py --check
    uv run scripts/generate_env_docs.py --update
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
BEGIN_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def get_env_table() -> str:
    from h4ckath0n.config import Settings

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"

        default_val = field.default
        if default_val == "" or default_val == []:
            default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{'true' if default_val else 'false'}`"
        else:
            default_str = f"`{default_val}`"

        desc = field.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def update_readme(table: str, check_only: bool) -> int:
    text = README.read_text(encoding="utf-8")

    if BEGIN_MARKER not in text or END_MARKER not in text:
        print(f"❌ {BEGIN_MARKER} or {END_MARKER} not found in README.md")
        return 1

    start_idx = text.find(BEGIN_MARKER) + len(BEGIN_MARKER)
    end_idx = text.find(END_MARKER)

    new_text = text[:start_idx] + "\n" + table + "\n" + text[end_idx:]

    if text == new_text:
        if check_only:
            print("✅ Environment variable documentation is up to date.")
        return 0

    if check_only:
        print("❌ Environment variable documentation in README.md is out of date.")
        print("Run `uv run scripts/generate_env_docs.py --update` to fix.")
        return 1

    README.write_text(new_text, encoding="utf-8")
    print("✅ Updated environment variable documentation in README.md.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    if not args.check and not args.update:
        print("Usage: generate_env_docs.py [--check | --update]")
        return 1

    src_dir = str(REPO_ROOT / "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    table = get_env_table()
    return update_readme(table, check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
