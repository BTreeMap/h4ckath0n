#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify and update environment variables documentation in README.md.

Usage (from repo root):
    uv run scripts/check_doc_env.py          # Check mode
    uv run scripts/check_doc_env.py --fix    # Update mode
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

BEGIN_MARKER = "<!-- BEGIN_ENV_VARS -->"
END_MARKER = "<!-- END_ENV_VARS -->"


def format_default(val: object) -> str:
    """Format a default value for the markdown table."""
    if val == "":
        return "empty"
    if val == []:
        return "`[]`"
    if isinstance(val, bool):
        return f"`{str(val).lower()}`"
    return f"`{val}`"


def generate_env_table() -> str:
    """Generate the markdown table for environment variables."""
    from h4ckath0n.config import Settings  # noqa: E402

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for name, field in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"
        default_repr = format_default(field.default)
        desc = field.description or ""
        lines.append(f"| `{env_name}` | {default_repr} | {desc} |")

    # Also inject the OpenAI keys manually since they do not strictly
    # map to H4CKATH0N_ settings in the same way
    lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")

    # We remove the custom extra H4CKATH0N_OPENAI_API_KEY that was in the original
    # docs if it's already generated above, or keep it if we want to ensure
    # full parity with the previous table manually:
    if "H4CKATH0N_OPENAI_API_KEY" not in [
        f"H4CKATH0N_{name.upper()}" for name in Settings.model_fields
    ]:
        lines.append(
            "| `H4CKATH0N_OPENAI_API_KEY` | empty | Alternate OpenAI API key for the LLM wrapper |"
        )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or update environment variables doc.")
    parser.add_argument("--fix", action="store_true", help="Update README.md inline")
    args = parser.parse_args()

    readme_text = README.read_text()

    if BEGIN_MARKER not in readme_text or END_MARKER not in readme_text:
        print(f"❌ Error: Could not find {BEGIN_MARKER} and/or {END_MARKER} in README.md.")
        return 1

    table_content = generate_env_table()

    # Isolate current block
    start_idx = readme_text.index(BEGIN_MARKER) + len(BEGIN_MARKER)
    end_idx = readme_text.index(END_MARKER)

    # Check if they are immediately adjacent
    current_content = readme_text[start_idx:end_idx].strip()

    if current_content == table_content:
        print("✅ Environment variables documentation is up-to-date.")
        return 0

    if args.fix:
        new_text = readme_text[:start_idx] + "\n" + table_content + "\n" + readme_text[end_idx:]
        README.write_text(new_text)
        print("🔧 Fixed environment variables documentation in README.md.")
        return 0

    print("❌ Environment variables documentation is out-of-date in README.md.")
    print("Run `uv run scripts/check_doc_env.py --fix` to update it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
