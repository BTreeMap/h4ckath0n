#!/usr/bin/env -S uv run python
"""Generate environment variable documentation from Pydantic Settings."""

import argparse
import sys
from pathlib import Path

# Add src to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / 'src'))

from h4ckath0n.config import Settings  # noqa: E402

README = REPO_ROOT / "README.md"
START_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"

def generate_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        var_name = f"`H4CKATH0N_{name.upper()}`"

        default = field.default
        if default == "" or default is None:
            default_str = "empty"
        elif default == [] or str(default) == "PydanticUndefined":
            default_str = "`[]`"
        else:
            default_str = f"`{default}`"

        # Handle booleans properly for bash
        if isinstance(default, bool):
            default_str = f"`{'true' if default else 'false'}`"

        # Special overrides to match old docs
        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"

        desc = field.description or ""
        lines.append(f"| {var_name} | {default_str} | {desc} |")

        # Also, openai_api_key needs an extra un-prefixed one based on previous readme
        if name == "openai_api_key":
            lines.insert(-1, "| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
            lines[-1] = (
                "| `H4CKATH0N_OPENAI_API_KEY` | empty | "
                "Alternate OpenAI API key for the LLM wrapper |"
            )

    return "\n".join(lines)

def update_readme(new_content: str, check_only: bool = False) -> int:
    readme_text = README.read_text()
    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        print("❌ Could not find BEGIN/END ENV VARS markers in README.md")
        return 1

    start_idx = readme_text.index(START_MARKER) + len(START_MARKER)
    end_idx = readme_text.index(END_MARKER)

    current_content = readme_text[start_idx:end_idx].strip()

    if current_content == new_content.strip():
        print("✅ README.md is up to date.")
        return 0

    if check_only:
        print("❌ README.md environment variables are out of date!")
        print("Run `uv run scripts/generate_env_docs.py --update` to fix.")
        return 1

    new_readme = (
        readme_text[:start_idx] +
        "\n" + new_content + "\n" +
        readme_text[end_idx:]
    )
    README.write_text(new_readme)
    print("✅ Updated README.md with latest environment variables.")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Generate env vars doc")
    parser.add_argument("--update", action="store_true", help="Update README.md")
    parser.add_argument("--check", action="store_true", help="Check if README.md is up to date")
    args = parser.parse_args()

    table = generate_table()

    if args.update or args.check:
        return update_readme(table, check_only=args.check)
    else:
        print(table)
        return 0

if __name__ == "__main__":
    sys.exit(main())
