#!/usr/bin/env -S uv run python
"""Generate the environment variables table for README.md and .env.example."""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import AliasChoices

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
ENV_EXAMPLE = REPO_ROOT / ".env.example"

ENV_START_MARKER = "<!-- ENV_START -->\n"
ENV_END_MARKER = "<!-- ENV_END -->\n"


def generate_env_table() -> str:
    from h4ckath0n.config import Settings

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for field_name, field_info in Settings.model_fields.items():
        alias = getattr(field_info, "validation_alias", None)
        aliases = []
        if isinstance(alias, AliasChoices):
            aliases = list(alias.choices)
        elif isinstance(alias, str):
            aliases = [alias]
        else:
            aliases = [f"H4CKATH0N_{field_name.upper()}"]

        var_str = "<br>".join(f"`{a}`" for a in aliases)
        default_val = field_info.default
        if default_val == "" or default_val == [] or default_val is None:
            default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{str(default_val).lower()}`"
        else:
            default_str = f"`{default_val}`"

        desc = field_info.description or ""
        lines.append(f"| {var_str} | {default_str} | {desc} |")

    return "\n".join(lines) + "\n"


def generate_env_example() -> str:
    from h4ckath0n.config import Settings

    lines = []
    for field_name, field_info in Settings.model_fields.items():
        alias = getattr(field_info, "validation_alias", None)
        if isinstance(alias, AliasChoices):
            primary = alias.choices[0]
        elif isinstance(alias, str):
            primary = alias
        else:
            primary = f"H4CKATH0N_{field_name.upper()}"

        desc = field_info.description or ""
        if desc:
            lines.append(f"# {desc}")

        default_val = field_info.default
        if default_val == "" or default_val == [] or default_val is None:
            val_str = ""
        elif isinstance(default_val, bool):
            val_str = str(default_val).lower()
        else:
            val_str = str(default_val)

        lines.append(f"{primary}={val_str}")
        lines.append("")

    return "\n".join(lines)


def update_readme(table_text: str) -> bool:
    content = README.read_text()
    if ENV_START_MARKER not in content or ENV_END_MARKER not in content:
        print(
            f"Error: missing {ENV_START_MARKER.strip()} or {ENV_END_MARKER.strip()} in README.md"
        )
        return False

    before = content.split(ENV_START_MARKER)[0]
    after = content.split(ENV_END_MARKER)[1]
    new_content = before + ENV_START_MARKER + table_text + ENV_END_MARKER + after

    if content != new_content:
        README.write_text(new_content)
        print("Updated README.md")
    else:
        print("README.md is up to date")
    return True


def main() -> int:
    table_text = generate_env_table()
    if not update_readme(table_text):
        return 1

    env_text = generate_env_example()
    if not ENV_EXAMPLE.exists() or ENV_EXAMPLE.read_text() != env_text:
        ENV_EXAMPLE.write_text(env_text)
        print("Updated .env.example")
    else:
        print(".env.example is up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
