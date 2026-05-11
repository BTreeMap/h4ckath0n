#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that env vars in README.md match pydantic Settings.

Usage (from repo root):
    uv run scripts/generate_env_docs.py --check
    uv run scripts/generate_env_docs.py --update
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
SRC_PATH = REPO_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))
from h4ckath0n.config import Settings  # noqa: E402

BEGIN_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def get_markdown_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            env_name = "OPENAI_API_KEY / H4CKATH0N_OPENAI_API_KEY"
        else:
            env_name = f"H4CKATH0N_{name.upper()}"

        desc = field.description or "TODO"

        default = field.default
        if default == "" or default is None:
            default_str = "empty"
        elif isinstance(default, bool):
            default_str = f"`{'true' if default else 'false'}`"
        elif isinstance(default, list):
            default_str = f"`{default}`".replace("'", '"')
        else:
            default_str = f"`{default}`"

        lines.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("--check", "--update"):
        print("Usage: scripts/generate_env_docs.py [--check|--update]")
        sys.exit(1)

    table = get_markdown_table()
    content = README.read_text()

    if BEGIN_MARKER not in content or END_MARKER not in content:
        print(f"Error: {BEGIN_MARKER} and {END_MARKER} not found in README.md")
        sys.exit(1)

    pattern = re.compile(f"({BEGIN_MARKER}\\n).*?({END_MARKER})", re.DOTALL)
    new_content = pattern.sub(f"\\1{table}\\n\\2", content)

    if sys.argv[1] == "--check":
        if content != new_content:
            print("❌ Environment variables in README.md are out of date.")
            print("Run `uv run scripts/generate_env_docs.py --update` to fix.")
            sys.exit(1)
        print("✅ Environment variables in README.md match configuration.")
    elif sys.argv[1] == "--update":
        README.write_text(new_content)
        print("✅ README.md updated with latest environment variables.")


if __name__ == "__main__":
    main()
