#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that config settings are accurately documented.

Usage (from repo root):
    uv run scripts/sync_config_docs.py [--check]

If --check is provided, it exits with 1 if the README is out of sync.
Otherwise, it updates the README with the generated configuration table.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pydantic_core import PydanticUndefined

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from h4ckath0n.config import Settings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_START -->"
END_MARKER = "<!-- CONFIG_END -->"


def generate_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
            lines.append(
                "| `H4CKATH0N_OPENAI_API_KEY` | empty | "
                "Alternate OpenAI API key for the LLM wrapper |"
            )
            continue

        env_name = f"H4CKATH0N_{name.upper()}"

        default = field.default
        if default is PydanticUndefined:
            default_factory = getattr(field, "default_factory", None)
            default = default_factory() if default_factory is not None else "required"

        if default == "":
            default = "empty"
        elif default is True:
            default = "`true`"
        elif default is False:
            default = "`false`"
        elif default == []:
            default = "`[]`"
        elif (isinstance(default, str) and default not in ("empty", "required")) or (
            isinstance(default, int) and not isinstance(default, bool)
        ):
            default = f"`{default}`"

        desc = field.description or ""

        lines.append(f"| `{env_name}` | {default} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if README is up-to-date")
    args = parser.parse_args()

    readme_text = README.read_text()

    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        print("❌ Markers not found in README.md")
        return 1

    start_idx = readme_text.find(START_MARKER) + len(START_MARKER)
    end_idx = readme_text.find(END_MARKER)

    current_section = readme_text[start_idx:end_idx].strip()
    new_section = generate_table().strip()

    if current_section == new_section:
        print("✅ Configuration documentation is up-to-date.")
        return 0

    if args.check:
        print("❌ Configuration documentation in README.md is out of sync!")
        print("Run `uv run scripts/sync_config_docs.py` to fix it.")
        return 1

    new_readme = readme_text[:start_idx] + "\n" + new_section + "\n" + readme_text[end_idx:]
    README.write_text(new_readme)
    print("✅ Updated configuration documentation in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
