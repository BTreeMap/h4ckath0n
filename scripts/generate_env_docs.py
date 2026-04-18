#!/usr/bin/env -S uv run python
"""Drift-prevention script to generate environment variable docs."""

import argparse
import sys
from pathlib import Path


def get_env_table() -> str:
    from h4ckath0n.config import Settings

    prefix = Settings.model_config.get("env_prefix", "H4CKATH0N_")
    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in Settings.model_fields.items():
        var_name = f"{prefix}{name}".upper()
        default = field.default

        if default == "":
            default_str = "empty"
        elif default == []:
            default_str = "`[]`"
        elif isinstance(default, bool):
            default_str = f"`{'true' if default else 'false'}`"
        else:
            default_str = f"`{default}`"

        desc = field.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {desc} |")

    # Special case for OpenAI API Key fallback
    lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    readme_path = repo_root / "README.md"

    content = readme_path.read_text()

    start_marker = "<!-- GENERATED_ENV_VARS_START -->"
    end_marker = "<!-- GENERATED_ENV_VARS_END -->"

    if start_marker not in content or end_marker not in content:
        print("Error: Missing generation markers in README.md")
        return 1

    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)

    table = get_env_table()
    new_content = content[:start_idx] + "\n" + table + "\n" + content[end_idx:]

    if args.check:
        if content != new_content:
            print("❌ README.md environment variables table is out of date.")
            print("Run `uv run scripts/generate_env_docs.py` to update it.")
            return 1
        print("✅ README.md environment variables table is up to date.")
        return 0

    readme_path.write_text(new_content)
    print("✅ README.md environment variables table updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
