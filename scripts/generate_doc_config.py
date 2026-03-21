#!/usr/bin/env -S uv run python
"""Drift-prevention script to generate the configuration table in README.md.

Usage (from repo root):
    uv run scripts/generate_doc_config.py [--check]
"""

import argparse
import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_TABLE_START -->"
END_MARKER = "<!-- CONFIG_TABLE_END -->"


def generate_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field_info in Settings.model_fields.items():
        # The Settings model already prefixes with H4CKATH0N_ via env_prefix.
        # But we handle OPENAI_API_KEY differently to match the original doc
        # where it is listed without the prefix, with an alternate version.

        var_name = f"H4CKATH0N_{name.upper()}"

        from pydantic_core import PydanticUndefined

        if field_info.default is not PydanticUndefined:
            default = field_info.default
        elif field_info.default_factory is not None:
            default = field_info.default_factory()
        else:
            default = None

        if default == "":
            default_str = "empty"
        elif default == []:
            default_str = "`[]`"
        elif isinstance(default, bool):
            default_str = f"`{'true' if str(default).lower() == 'true' else 'false'}`"
        else:
            default_str = f"`{default}`"

        description = field_info.description or ""
        # In development mode, RP_ID and ORIGIN fall back to localhost defaults.
        if name == "rp_id":
            default_str = "`localhost` in development"
        if name == "origin":
            default_str = "`http://localhost:8000` in development"

        if name == "openai_api_key":
            lines.append(f"| `OPENAI_API_KEY` | {default_str} | {description} |")
            lines.append(
                f"| `H4CKATH0N_OPENAI_API_KEY` | {default_str} | Alternate {description} |"
            )
        else:
            lines.append(f"| `{var_name}` | {default_str} | {description} |")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if README.md is up to date")
    args = parser.parse_args()

    table = generate_table()
    content = README.read_text()

    if START_MARKER not in content or END_MARKER not in content:
        print("❌ Markers not found in README.md")
        return 1

    start_idx = content.find(START_MARKER) + len(START_MARKER)
    end_idx = content.find(END_MARKER)

    new_content = content[:start_idx] + "\n" + table + "\n" + content[end_idx:]

    if args.check:
        if content != new_content:
            print(
                "❌ Configuration table in README.md is out of date.\n"
                "Run 'uv run scripts/generate_doc_config.py' to update it."
            )
            return 1
        print("✅ Configuration table in README.md is up to date.")
        return 0
    else:
        README.write_text(new_content)
        print("✅ Updated configuration table in README.md.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
