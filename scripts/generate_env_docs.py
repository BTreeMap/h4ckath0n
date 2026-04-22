#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables in README.md are generated
from the config.py Settings class.

Usage (from repo root):
    uv run scripts/generate_env_docs.py [--check]
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- GENERATED_ENV_VARS_START -->"
END_MARKER = "<!-- GENERATED_ENV_VARS_END -->"


def generate_table() -> str:
    from h4ckath0n.config import Settings

    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for field_name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{field_name.upper()}"

        if field_name == "openai_api_key":
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")

        default_val = field_info.default
        if default_val == "":
            default_str = "empty"
        elif default_val == []:
            default_str = "`[]`"
        elif isinstance(default_val, bool):
            default_str = f"`{'true' if default_val else 'false'}`"
        elif isinstance(default_val, int) or default_val is not None:
            default_str = f"`{default_val}`"
        else:
            default_str = "empty"

        desc = field_info.description or ""

        # Override descriptions for edge cases as currently in README
        if field_name == "rp_id":
            desc = "WebAuthn relying party ID, required in production"
            default_str = "`localhost` in development"
        elif field_name == "origin":
            desc = "WebAuthn origin, required in production"
            default_str = "`http://localhost:8000` in development"

        lines.append(f"| `{var_name}` | {default_str} | {desc} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    readme_text = README.read_text()

    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        print("❌ README.md must contain the START and END markers for generated env vars.")
        return 1

    pattern = re.compile(rf"{START_MARKER}.*?{END_MARKER}", re.DOTALL)
    current_section = pattern.search(readme_text).group(0)

    table_content = generate_table()
    new_section = f"{START_MARKER}\n{table_content}\n{END_MARKER}"

    if args.check:
        if current_section != new_section:
            print(
                "❌ Environment variables documentation in README.md is out of sync "
                "with Settings in src/h4ckath0n/config.py."
            )
            print("Run 'uv run scripts/generate_env_docs.py' to update it.")
            return 1
        print("✅ Environment variables documentation is up to date.")
        return 0

    if current_section != new_section:
        new_readme_text = readme_text.replace(current_section, new_section)
        README.write_text(new_readme_text)
        print("✅ Updated environment variables documentation in README.md.")
    else:
        print("✅ Environment variables documentation in README.md is already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
