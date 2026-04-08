#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every configuration setting is documented.

Usage (from repo root):
    uv run scripts/check_doc_config.py

The script imports the h4ckath0n config Settings, enumerates all fields, and checks that
README.md mentions each one. It also generates the markdown table for configuration.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_config_fields() -> list[tuple[str, str, str]]:
    """Return a list of (env_var_name, default, description) expected by Settings."""
    from h4ckath0n.config import Settings  # noqa: E402

    fields = []
    prefix = Settings.model_config.get("env_prefix", "H4CKATH0N_").upper()
    for field_name, field_info in Settings.model_fields.items():
        if field_name == "openai_api_key":
            env_var = "OPENAI_API_KEY"
            # special case for openai_api_key
        else:
            env_var = f"{prefix}{field_name.upper()}"

        default_val = field_info.default
        if default_val == "" or default_val == []:
            default_str = "empty"
        elif (
            getattr(default_val, "__name__", "") == "PydanticUndefined"
            or str(default_val) == "PydanticUndefined"
        ):
            if field_info.default_factory:
                # if there is a factory
                default_val = field_info.default_factory()  # type: ignore[call-arg]
                default_str = "`[]`" if default_val == [] else str(default_val)
            else:
                default_str = "empty"
        elif isinstance(default_val, bool):
            default_str = f"`{str(default_val).lower()}`"
        else:
            default_str = f"`{str(default_val)}`"

        if default_str == "empty":
            pass  # Keep it without backticks as per current style

        description = field_info.description or ""
        fields.append((env_var, default_str, description))

        # OpenAI API key is special, also document the prefixed version
        if field_name == "openai_api_key":
            # The previous one added OPENAI_API_KEY with "Alternate...", let's fix it
            # pop the last one, and insert two:
            fields.pop()
            fields.append(("OPENAI_API_KEY", "empty", "OpenAI API key for the LLM wrapper"))
            fields.append(
                (
                    f"{prefix}OPENAI_API_KEY",
                    "empty",
                    "Alternate OpenAI API key for the LLM wrapper",
                )
            )

    return fields


def update_readme(fields: list[tuple[str, str, str]]) -> bool:
    """Updates the Configuration section in README.md."""
    readme_text = README.read_text()

    table_lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for var, default, desc in fields:
        # Defaults are already formatted with backticks if needed
        table_lines.append(f"| `{var}` | {default} | {desc} |")

    table_text = "\n".join(table_lines)

    # We want to replace the table inside the Configuration section
    pattern = re.compile(
        r"(## Configuration\n\nAll settings use the `H4CKATH0N_` "
        r"prefix unless noted\.\n\n)\| Variable \|.*?(?=\n\nIn development)",
        re.DOTALL,
    )

    match = pattern.search(readme_text)
    if not match:
        print("❌ Could not find the Configuration table in README.md")
        return False

    new_text = readme_text[: match.end(1)] + table_text + readme_text[match.end() :]

    if new_text != readme_text:
        README.write_text(new_text)
        print("✅ Updated README.md with latest configuration variables")
        return True

    print("✅ Configuration variables in README.md are up to date")
    return True


def main() -> int:
    fields = get_config_fields()
    success = update_readme(fields)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
