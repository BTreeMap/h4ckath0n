#!/usr/bin/env -S uv run python
"""Verify that every ``Settings`` environment variable is documented in the README."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
ENV_EXAMPLE = (
    REPO_ROOT
    / "packages"
    / "create-h4ckath0n"
    / "templates"
    / "fullstack"
    / "web"
    / ".env.example"
)

_ENV_DOCS_MARKER_START = "<!-- env-docs:start -->\n"
_ENV_DOCS_MARKER_END = "<!-- env-docs:end -->\n"


def generate_docs() -> tuple[str, str]:
    from h4ckath0n.config import Settings

    table_lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    env_lines = []

    for field_name, field_info in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{field_name.upper()}"

        # Format default
        default = field_info.default
        if default is None or default == "":
            default_str = "empty"
        elif isinstance(default, bool):
            default_str = "`true`" if default else "`false`"
        elif isinstance(default, list):
            default_str = "`[]`"
        else:
            default_str = f"`{default}`"

        desc = field_info.description or ""

        if env_name == "H4CKATH0N_RP_ID":
            default_str = "`localhost` in development"
        elif env_name == "H4CKATH0N_ORIGIN":
            default_str = "`http://localhost:8000` in development"

        table_lines.append(f"| `{env_name}` | {default_str} | {desc} |")

        # Special case: add OPENAI_API_KEY manually like the current docs have
        if env_name == "H4CKATH0N_OPENAI_API_KEY":
            table_lines.insert(
                -1, "| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |"
            )

        # Format .env.example
        env_lines.append(f"# {desc}")

        # Determine example value
        example_val = default if default != "" else ""
        if isinstance(default, bool):
            example_val = "true" if default else "false"
        elif isinstance(default, list):
            example_val = "[]"
        env_lines.append(f"{env_name}={example_val}")
        env_lines.append("")

    return "\n".join(table_lines) + "\n", "\n".join(env_lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    table_content, env_content = generate_docs()

    readme_text = README.read_text()

    start_idx = readme_text.find(_ENV_DOCS_MARKER_START)
    end_idx = readme_text.find(_ENV_DOCS_MARKER_END)

    if start_idx == -1 or end_idx == -1:
        print("Error: Could not find env-docs markers in README.md")
        return 1

    current_table = readme_text[start_idx + len(_ENV_DOCS_MARKER_START) : end_idx]

    if current_table != table_content:
        if args.update:
            new_readme = (
                readme_text[: start_idx + len(_ENV_DOCS_MARKER_START)]
                + table_content
                + readme_text[end_idx:]
            )
            README.write_text(new_readme)
            print("Updated README.md")
        else:
            print("❌ Environment variable documentation in README.md is out of sync.")
            print("Run `uv run scripts/check_doc_env.py --update` to fix.")
            return 1
    else:
        print("✅ Environment variable documentation in README.md is up to date.")

    if ENV_EXAMPLE.exists():
        current_env = ENV_EXAMPLE.read_text()
        if current_env != env_content:
            if args.update:
                ENV_EXAMPLE.write_text(env_content)
                print(f"Updated {ENV_EXAMPLE.relative_to(REPO_ROOT)}")
            else:
                print(f"❌ {ENV_EXAMPLE.relative_to(REPO_ROOT)} is out of sync.")
                print("Run `uv run scripts/check_doc_env.py --update` to fix.")
                return 1
        else:
            print(f"✅ {ENV_EXAMPLE.relative_to(REPO_ROOT)} is up to date.")
    elif args.update:
        ENV_EXAMPLE.parent.mkdir(parents=True, exist_ok=True)
        ENV_EXAMPLE.write_text(env_content)
        print(f"Created {ENV_EXAMPLE.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
