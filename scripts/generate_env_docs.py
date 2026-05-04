#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that env vars in config.py match README.md."""

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
BEGIN_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def generate_table() -> str:
    from h4ckath0n.config import Settings

    fields = Settings.model_fields

    lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in fields.items():
        var_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            var_name = f"`{var_name}` or `OPENAI_API_KEY`"
        else:
            var_name = f"`{var_name}`"

        default = field.default
        if default == "":
            default_str = "empty"
        elif default is False:
            default_str = "`false`"
        elif default is True:
            default_str = "`true`"
        elif default == []:
            default_str = "`[]`"
        else:
            default_str = f"`{default}`"

        if name == "rp_id":
            default_str = "`localhost` in development"
        if name == "origin":
            default_str = "`http://localhost:8000` in development"

        desc = field.description or ""

        lines.append(f"| {var_name} | {default_str} | {desc} |")

    return "\n".join(lines)


def update_readme():
    text = README.read_text()
    if BEGIN_MARKER not in text or END_MARKER not in text:
        print("Markers not found in README.md")
        return False

    start = text.index(BEGIN_MARKER) + len(BEGIN_MARKER)
    end = text.index(END_MARKER)

    new_text = text[:start] + "\n" + generate_table() + "\n" + text[end:]
    README.write_text(new_text)
    return True


def check_readme():
    text = README.read_text()
    if BEGIN_MARKER not in text or END_MARKER not in text:
        print("Markers not found in README.md")
        return False

    start = text.index(BEGIN_MARKER) + len(BEGIN_MARKER)
    end = text.index(END_MARKER)

    current_table = text[start:end].strip()
    expected_table = generate_table().strip()

    return current_table == expected_table


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    sys.path.insert(0, str(REPO_ROOT / "src"))

    if args.update:
        if update_readme():
            print("README.md updated.")
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.check:
        if check_readme():
            print("✅ Environment variables in README.md are up to date.")
            sys.exit(0)
        else:
            print("❌ Environment variables in README.md are out of date.")
            print("Run `uv run scripts/generate_env_docs.py --update` to fix.")
            sys.exit(1)
    else:
        print("Usage: --update or --check")
        sys.exit(1)
