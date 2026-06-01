#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that environment variables are documented in README.md.

Usage (from repo root):
    uv run scripts/check_doc_env_vars.py [--update]
"""

from __future__ import annotations

import sys
from pathlib import Path

# Fix: Ensure correct imports and Pydantic field parsing logic
try:
    from pydantic_core import PydanticUndefined
except ImportError:
    # Handle older pydantic versions if needed
    class _PydanticUndefined:
        pass

    PydanticUndefined = _PydanticUndefined()


REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
BEGIN_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def get_env_vars_table() -> str:
    from h4ckath0n.config import Settings

    # We parse the Pydantic model fields correctly.
    # The instruction says: use `field.is_required()` to identify required fields without defaults,
    # and check `field.default_factory` for dynamic defaults, rather than checking
    # `field_info.default` for the `PydanticUndefined` sentinel type.

    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"

        # Handle OPENAI_API_KEY special case
        if name == "openai_api_key":
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")

        if field.is_required():
            default_str = "required"
        elif field.default_factory is not None:
            if field.default_factory is list:
                default_str = "`[]`"
            elif field.default_factory is dict:
                default_str = "`{}`"
            else:
                default_str = "dynamic"
        else:
            if field.default == "":
                default_str = "empty"
            elif field.default is None:
                default_str = "`null`"
            elif isinstance(field.default, bool):
                default_str = f"`{'true' if field.default else 'false'}`"
            elif isinstance(field.default, str):
                default_str = f"`{field.default}`"
            else:
                default_str = f"`{field.default}`"

        desc = field.description or "No description provided."

        # Add a special note for RP_ID and ORIGIN since they have special defaults in dev
        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"

        lines.append(f"| `{var_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    try:
        import h4ckath0n.config  # noqa: F401
    except ImportError:
        print(
            "❌ Cannot import h4ckath0n.config. Run from project root using uv run.",
            file=sys.stderr,
        )
        return 1

    table_content = get_env_vars_table()

    readme_text = README.read_text()

    if BEGIN_MARKER not in readme_text or END_MARKER not in readme_text:
        print("❌ README.md must contain the following markers for env vars:")
        print(f"  {BEGIN_MARKER}")
        print(f"  {END_MARKER}")
        print("\nPlease add them to the Configuration section of README.md.")
        return 1

    start_idx = readme_text.find(BEGIN_MARKER) + len(BEGIN_MARKER)
    end_idx = readme_text.find(END_MARKER)

    current_content = readme_text[start_idx:end_idx].strip()

    if current_content == table_content:
        print("✅ Environment variables documentation is up-to-date.")
        return 0

    if "--update" in sys.argv:
        new_readme = readme_text[:start_idx] + "\n" + table_content + "\n" + readme_text[end_idx:]
        README.write_text(new_readme)
        print("✨ Updated README.md with latest environment variables.")
        return 0
    else:
        print("❌ Environment variables documentation is out-of-date!")
        print("Run `uv run scripts/check_doc_env_vars.py --update` to fix it.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
