#!/usr/bin/env -S uv run python
"""Drift-prevention check: generate config env vars in README.md."""

import re
import sys
from pathlib import Path

# Add src to sys.path to allow importing h4ckath0n
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from h4ckath0n.config import Settings  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for field_name, field_info in Settings.model_fields.items():
        var_name = f"`H4CKATH0N_{field_name.upper()}`"
        if field_name == "openai_api_key":
            var_name = "`OPENAI_API_KEY`"

        default_val = field_info.default
        if default_val == "":
            default_val_str = "empty"
        elif isinstance(default_val, bool):
            default_val_str = f"`{str(default_val).lower()}`"
        elif isinstance(default_val, list) and not default_val:
            default_val_str = "`[]`"
        elif field_name == "rp_id":
            default_val_str = "`localhost` in development"
        elif field_name == "origin":
            default_val_str = "`http://localhost:8000` in development"
        else:
            default_val_str = f"`{default_val}`"

        desc = field_info.description or ""
        lines.append(f"| {var_name} | {default_val_str} | {desc} |")

        if field_name == "openai_api_key":
            lines.append(
                "| `H4CKATH0N_OPENAI_API_KEY` | empty | Alternate API key for the LLM wrapper |"
            )

    return "\n".join(lines) + "\n"


def main() -> int:
    check_only = "--check" in sys.argv
    readme_text = README.read_text(encoding="utf-8")

    start_marker = "<!-- CONFIG_DOCS_START -->\n"
    end_marker = "<!-- CONFIG_DOCS_END -->"

    pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
    if not pattern.search(readme_text):
        print("❌ Could not find CONFIG_DOCS markers in README.md")
        return 1

    new_table = generate_table()
    replacement = f"{start_marker}{new_table}{end_marker}"
    new_readme = pattern.sub(replacement, readme_text)

    if readme_text == new_readme:
        print("✅ README.md config documentation is up to date.")
        return 0

    if check_only:
        print(
            "❌ README.md config documentation is out of date. "
            "Run `uv run scripts/generate_config_docs.py` to update."
        )
        return 1

    README.write_text(new_readme, encoding="utf-8")
    print("✅ Updated README.md config documentation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
