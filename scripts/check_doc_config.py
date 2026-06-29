#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all configuration fields in Settings
are documented in README.md.

Usage:
    uv run scripts/check_doc_config.py [--update]
"""

import re
import sys
from pathlib import Path

from pydantic_core import PydanticUndefined

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from h4ckath0n.config import Settings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_config_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            env_name = "OPENAI_API_KEY"

        default_val = field.default
        if default_val == PydanticUndefined:
            default_val = getattr(field, "default_factory", None)
            if default_val:
                default_val = default_val()

        if default_val == "":
            default_val = "empty"
        elif isinstance(default_val, bool):
            default_val = f"`{str(default_val).lower()}`"
        elif isinstance(default_val, list) or default_val is not None and default_val != "empty":
            default_val = f"`{default_val}`"

        description = field.description or ""
        if name == "rp_id":
            default_val = "`localhost` in development"
        if name == "origin":
            default_val = "`http://localhost:8000` in development"
        lines.append(f"| `{env_name}` | {default_val} | {description} |")
        if name == "openai_api_key":
            lines.append(
                "| `H4CKATH0N_OPENAI_API_KEY` | empty | "
                "Alternate OpenAI API key for the LLM wrapper |"
            )
    return "\n".join(lines)


def main() -> int:
    update_mode = "--update" in sys.argv
    readme_text = README.read_text()

    start_marker = "<!-- CONFIG_START -->"
    end_marker = "<!-- CONFIG_END -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Could not find CONFIG_START and CONFIG_END markers in README.md")
        return 1

    table_content = generate_config_table()
    new_text = re.sub(
        f"{start_marker}.*?{end_marker}",
        f"{start_marker}\n{table_content}\n{end_marker}",
        readme_text,
        flags=re.DOTALL,
    )

    if new_text == readme_text:
        print("✅ README.md configuration is up to date.")
        return 0

    if update_mode:
        README.write_text(new_text)
        print("✅ Updated README.md with latest configuration.")
        return 0
    else:
        print(
            "❌ README.md configuration is out of date. "
            "Run `uv run scripts/check_doc_config.py --update`."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
