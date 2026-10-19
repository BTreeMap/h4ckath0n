#!/usr/bin/env -S uv run python
"""Drift-prevention check: generate and verify environment variables."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from pydantic import AliasChoices

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
ENV_EXAMPLE = REPO_ROOT / ".env.example"


def get_env_vars() -> list[tuple[str, str, str, str]]:
    from h4ckath0n.config import Settings

    vars_info = []
    for name, field in Settings.model_fields.items():
        if isinstance(field.validation_alias, AliasChoices):
            for choice in field.validation_alias.choices:
                desc_suffix = (
                    " (Alternate)"
                    if choice != field.validation_alias.choices[0]
                    else ""
                )
                primary_name = str(choice)
                env_name = primary_name
                default = field.default
                default_str = (
                    "empty"
                    if default == ""
                    else "`true`"
                    if default is True
                    else "`false`"
                    if default is False
                    else "`[]`"
                    if isinstance(default, list)
                    else f"`{default}`"
                )
                desc = field.description or ""
                if desc_suffix and "Alternate" not in desc:
                    desc = "Alternate " + desc
                vars_info.append((env_name, primary_name, default_str, desc))
        else:
            env_name = f"H4CKATH0N_{name.upper()}"
            primary_name = env_name
            default = field.default
            default_str = (
                "empty"
                if default == ""
                else "`true`"
                if default is True
                else "`false`"
                if default is False
                else "`[]`"
                if isinstance(default, list)
                else f"`{default}`"
            )
            desc = field.description or ""
            vars_info.append((env_name, primary_name, default_str, desc))
    return vars_info


def generate_markdown(vars_info: list[tuple[str, str, str, str]]) -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for env_name, _primary_name, default_str, desc in vars_info:
        lines.append(f"| `{env_name}` | {default_str} | {desc} |")
    return "\n".join(lines)


def generate_env_example(vars_info: list[tuple[str, str, str, str]]) -> str:
    lines = []
    for _env_name, primary_name, _default_str, desc in vars_info:
        lines.append(f"# {desc}")
        lines.append(f"{primary_name}=")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()

    vars_info = get_env_vars()
    md_table = generate_markdown(vars_info)
    env_content = generate_env_example(vars_info)

    readme_text = README.read_text()
    match = re.search(
        r"<!-- BEGIN ENV_TABLE -->\n(.*?)\n<!-- END ENV_TABLE -->",
        readme_text,
        re.DOTALL,
    )
    if not match:
        print("❌ Could not find ENV_TABLE markers in README.md")
        return 1

    current_md_table = match.group(1).strip()

    current_env_content = ""
    if ENV_EXAMPLE.exists():
        current_env_content = ENV_EXAMPLE.read_text()

    if current_md_table != md_table.strip() or current_env_content != env_content:
        if args.fix:
            new_readme_text = (
                readme_text[: match.start(1)]
                + md_table
                + "\n"
                + readme_text[match.end(1) :]
            )
            README.write_text(new_readme_text)
            ENV_EXAMPLE.write_text(env_content)
            print("✅ Generated tables and .env.example")
            return 0
        else:
            print(
                "❌ Documentation drift detected! Run `uv run scripts/check_doc_env.py --fix`"
            )
            return 1

    print("✅ Environment documentation is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
