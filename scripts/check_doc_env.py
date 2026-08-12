#!/usr/bin/env -S uv run python
"""Drift-prevention check: Verify and auto-update environment variables in README.md."""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
MARKER_START = "<!-- BEGIN ENV VARS -->"
MARKER_END = "<!-- END ENV VARS -->"


def get_env_table() -> str:
    from h4ckath0n.config import Settings

    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        name_upper = name.upper()
        env_name = f"H4CKATH0N_{name_upper}"
        if name == "openai_api_key":
            env_name = "OPENAI_API_KEY / H4CKATH0N_OPENAI_API_KEY"

        default = field.default if field.default != "" else "empty"
        if default == []:
            default = "`[]`"
        elif isinstance(default, str) and default != "empty":
            default = f"`{default}`"
        elif isinstance(default, bool):
            default = f"`{'true' if default else 'false'}`"
        elif isinstance(default, int):
            default = f"`{default}`"

        desc = field.description or "TBD"
        lines.append(f"| `{env_name}` | {default} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    fix = "--fix" in sys.argv
    readme_text = README.read_text()

    if MARKER_START not in readme_text or MARKER_END not in readme_text:
        print("❌ Markers not found in README.md")
        return 1

    table = get_env_table()
    replacement = f"{MARKER_START}\n{table}\n{MARKER_END}"

    pattern = re.compile(rf"{MARKER_START}.*?{MARKER_END}", re.DOTALL)
    new_text = pattern.sub(replacement, readme_text)

    if new_text != readme_text:
        if fix:
            README.write_text(new_text)
            print("✅ Updated environment variables in README.md")
            return 0
        else:
            print("❌ README.md environment variables are out of date. Run with --fix.")
            return 1

    print("✅ Environment variables in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
