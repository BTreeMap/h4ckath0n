#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every env var in Settings is documented.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py [--update]
"""

import argparse
import re
import sys
from pathlib import Path

from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_START = "<!-- BEGIN ENV VARS -->"
MARKER_END = "<!-- END ENV VARS -->"


def generate_table() -> str:
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"

        default = "empty"
        if not field.is_required() and field.default is not None:
            # We explicitly handle PydanticUndefined which occurs with default_factory
            if (
                hasattr(field.default, "__class__")
                and field.default.__class__.__name__ == "PydanticUndefinedType"
            ):
                default = "`[]`" if field.default_factory is list else "empty"
            else:
                default = f"`{field.default}`"
                if isinstance(field.default, bool):
                    default = f"`{'true' if field.default else 'false'}`"
                elif isinstance(field.default, list):
                    default = "`[]`"
                elif name == "max_upload_bytes":
                    default = "`52428800`"
        elif not field.is_required() and field.default_factory is not None:
            # Evaluate default_factory for list
            default = "`[]`" if field.default_factory is list else "empty"
        elif field.default_factory is not None:
            default = "`[]`" if field.default_factory is list else "empty"

        # Hardcode the alternate openai key that exists in README but not in Settings directly
        if name == "openai_api_key":
            lines.append(f"| `OPENAI_API_KEY` | empty | {field.description or ''} |")
            var_name = "H4CKATH0N_OPENAI_API_KEY"
            desc = "Alternate OpenAI API key for the LLM wrapper"
            lines.append(f"| `{var_name}` | {default} | {desc} |")
            continue

        desc = field.description or ""
        lines.append(f"| `{var_name}` | {default} | {desc} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    table = generate_table()
    content = README.read_text(encoding="utf-8")

    pattern = re.compile(rf"{re.escape(MARKER_START)}.*{re.escape(MARKER_END)}", re.DOTALL)

    if not pattern.search(content):
        print(f"❌ Markers {MARKER_START} and {MARKER_END} not found in README.md")
        return 1

    new_content = pattern.sub(f"{MARKER_START}\n{table}\n{MARKER_END}", content)

    if content == new_content:
        print("✅ Environment variables table in README.md is up to date.")
        return 0

    if args.update:
        README.write_text(new_content, encoding="utf-8")
        print("✅ Updated environment variables table in README.md.")
        return 0

    print("❌ Environment variables table in README.md is out of date.")
    print("Run `uv run scripts/check_doc_env_vars.py --update` to fix.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
