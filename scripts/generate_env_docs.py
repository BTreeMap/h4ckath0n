#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all configuration options are documented in README.md.

Usage (from repo root):
    uv run scripts/generate_env_docs.py --update
    uv run scripts/generate_env_docs.py --check
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Add src to sys.path to allow imports from local source tree
SRC_PATH = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_PATH))

from h4ckath0n.config import Settings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def format_default(val: Any) -> str:
    """Format default value for display in markdown."""
    if val == "":
        return "empty"
    if isinstance(val, list):
        if not val:
            return "`[]`"
        return f"`{json.dumps(val)}`"
    if isinstance(val, bool):
        return f"`{str(val).lower()}`"
    return f"`{val}`"


def generate_table() -> str:
    """Generate the markdown table based on Settings."""
    rows = []
    rows.append("| Variable | Default | Description |")
    rows.append("|---|---|---|")

    for field_name, field_info in Settings.model_fields.items():
        env_var_name = f"H4CKATH0N_{field_name.upper()}"
        default_val = format_default(field_info.default)
        desc = field_info.description or ""

        # specific hardcoded additions based on existing docs to not break them
        if env_var_name == "H4CKATH0N_RP_ID":
            default_val = "`localhost` in development"
        elif env_var_name == "H4CKATH0N_ORIGIN":
            default_val = "`http://localhost:8000` in development"

        rows.append(f"| `{env_var_name}` | {default_val} | {desc} |")

    # Also add OPENAI_API_KEY as it's documented but not prefixed
    rows.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")

    return "\n".join(rows) + "\n"


def update_readme() -> None:
    readme_text = README.read_text(encoding="utf-8")
    table = generate_table()

    # We use a non-greedy match to replace everything between markers
    pattern = re.compile(r"(<!-- BEGIN ENV VARS -->\n).*?(<!-- END ENV VARS -->)", re.DOTALL)

    if not pattern.search(readme_text):
        print(
            "❌ Could not find <!-- BEGIN ENV VARS --> and <!-- END ENV VARS --> "
            "markers in README.md."
        )
        sys.exit(1)

    new_text = pattern.sub(rf"\g<1>{table}\g<2>", readme_text)
    README.write_text(new_text, encoding="utf-8")
    print("✅ README.md updated successfully.")


def check_readme() -> None:
    readme_text = README.read_text(encoding="utf-8")
    table = generate_table()

    pattern = re.compile(r"(<!-- BEGIN ENV VARS -->\n)(.*?)(<!-- END ENV VARS -->)", re.DOTALL)

    match = pattern.search(readme_text)
    if not match:
        print(
            "❌ Could not find <!-- BEGIN ENV VARS --> and <!-- END ENV VARS --> "
            "markers in README.md."
        )
        sys.exit(1)

    current_table = match.group(2)
    if current_table != table:
        print("❌ Configuration documentation in README.md is out of sync with Settings.")
        print("Run `uv run scripts/generate_env_docs.py --update` to fix it.")
        sys.exit(1)

    print("✅ Configuration documentation is up to date.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--update", action="store_true", help="Update README.md with generated env docs"
    )
    group.add_argument(
        "--check", action="store_true", help="Check if README.md env docs are up to date"
    )

    args = parser.parse_args()

    if args.update:
        update_readme()
    elif args.check:
        check_readme()
