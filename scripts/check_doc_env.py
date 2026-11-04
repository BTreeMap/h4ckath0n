#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify README.md env vars and .env.example are up to date."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
ENV_EXAMPLE = REPO_ROOT / ".env.example"


def get_default_value(field_info):
    from pydantic_core import PydanticUndefined

    val = field_info.default
    if val is PydanticUndefined and field_info.default_factory is not None:
        return field_info.default_factory()
    return val


def format_default(val: any) -> str:
    if val == "":
        return "empty"
    if val is False:
        return "`false`"
    if val is True:
        return "`true`"
    if val == []:
        return "`[]`"
    return f"`{val}`"


def generate_markdown_table() -> str:
    from h4ckath0n.config import Settings

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for field_name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{field_name.upper()}"
        default = format_default(get_default_value(field_info))
        if field_name == "openai_api_key":
            lines.append(
                "| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |"
            )
        desc = field_info.description or ""

        # Localize specific default displays to match existing README if possible
        if field_name == "rp_id":
            default = "`localhost` in development"
        elif field_name == "origin":
            default = "`http://localhost:8000` in development"

        lines.append(f"| `{var_name}` | {default} | {desc} |")
    return "\n".join(lines)


def generate_env_example() -> str:
    from h4ckath0n.config import Settings

    lines = ["# Auto-generated .env.example"]
    for field_name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{field_name.upper()}"
        desc = field_info.description or ""

        default_val = get_default_value(field_info)
        if default_val == "":
            default_str = ""
        elif isinstance(default_val, bool):
            default_str = str(default_val).lower()
        elif isinstance(default_val, list):
            default_str = json.dumps(default_val)
        else:
            default_str = str(default_val)

        if field_name == "openai_api_key":
            lines.append("# OpenAI API key for the LLM wrapper")
            lines.append("OPENAI_API_KEY=")
            lines.append("")

        if desc:
            lines.append(f"# {desc}")
        lines.append(f"{var_name}={default_str}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()

    expected_table = generate_markdown_table()
    expected_env = generate_env_example()

    readme_content = README.read_text()
    pattern = re.compile(
        r"<!-- START_ENV_DOCS -->\n.*?\n<!-- END_ENV_DOCS -->", re.DOTALL
    )

    if not pattern.search(readme_content):
        print(
            "❌ README.md is missing <!-- START_ENV_DOCS --> and <!-- END_ENV_DOCS --> markers."
        )
        return 1

    expected_readme = pattern.sub(
        f"<!-- START_ENV_DOCS -->\n{expected_table}\n<!-- END_ENV_DOCS -->",
        readme_content,
    )

    env_content = ENV_EXAMPLE.read_text() if ENV_EXAMPLE.exists() else ""

    drift_found = False
    if readme_content != expected_readme:
        print("❌ README.md is out of sync with Settings.")
        drift_found = True
    if env_content != expected_env:
        print("❌ .env.example is out of sync with Settings.")
        drift_found = True

    if drift_found:
        if args.fix:
            README.write_text(expected_readme)
            ENV_EXAMPLE.write_text(expected_env)
            print("✅ Fixed drift in README.md and .env.example.")
            return 0
        else:
            print("Run `uv run scripts/check_doc_env.py --fix` to update.")
            return 1

    print("✅ All environment variables are documented and .env.example is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
