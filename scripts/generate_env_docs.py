#!/usr/bin/env -S uv run python
"""Drift-prevention check: generate env var docs from Pydantic config."""

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
    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            var_name = "`OPENAI_API_KEY`"
        else:
            var_name = f"`H4CKATH0N_{name.upper()}`"

        default = field.default
        if default == "":
            default = "empty"
        elif default == []:
            default = "`[]`"
        elif default is False:
            default = "`false`"
        elif default is True:
            default = "`true`"
        elif isinstance(default, str) and default != "empty":
            default = f"`{default}`"

        desc = field.description or ""
        lines.append(f"| {var_name} | {default} | {desc} |")

        # Add the alternate openai key to match existing docs
        if name == "openai_api_key":
            lines.append(
                "| `H4CKATH0N_OPENAI_API_KEY` | empty | "
                "Alternate OpenAI API key for the LLM wrapper |"
            )

    return "\n".join(lines)


def update_readme(check_only: bool = False) -> int:
    readme_text = README.read_text()
    table = generate_table()

    pattern = re.compile(rf"{START_MARKER}.*?{END_MARKER}", re.DOTALL)
    if not pattern.search(readme_text):
        print("❌ Markers not found in README.md")
        return 1

    new_text = pattern.sub(f"{START_MARKER}\n{table}\n{END_MARKER}", readme_text)

    if check_only:
        if new_text != readme_text:
            print("❌ Env var docs are out of date. Run scripts/generate_env_docs.py")
            return 1
        print("✅ Env var docs are up to date.")
        return 0

    README.write_text(new_text)
    print("✅ Env var docs updated.")
    return 0


if __name__ == "__main__":
    check = "--check" in sys.argv
    sys.exit(update_readme(check))
