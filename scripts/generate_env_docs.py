#!/usr/bin/env -S uv run python
"""Drift-prevention check: enforce parity between config.py and README.md env vars."""

import argparse
import sys
from pathlib import Path

# Add src to sys.path so we can import from h4ckath0n
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- GENERATED_ENV_VARS_START -->\n"
END_MARKER = "<!-- GENERATED_ENV_VARS_END -->\n"


def generate_table() -> str:
    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]
    for name, field in Settings.model_fields.items():
        env_name = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            # Special case for OpenAI API Key (multiple vars)
            lines.append(f"| `OPENAI_API_KEY` | empty | {field.description} |")
            lines.append(f"| `{env_name}` | empty | Alternate {field.description} |")
            continue

        default_val = field.default if field.default_factory is None else "[]"
        default_str = (
            f"`{default_val}`" if not isinstance(default_val, str) or default_val else "empty"
        )
        if isinstance(default_val, str) and default_val:
            default_str = f"`{default_val}`"

        if name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"
        elif name == "auto_upgrade":
            default_str = "`false`"
        elif (
            name == "password_auth_enabled" or name == "first_user_is_admin" or name == "demo_mode"
        ):
            default_str = "`false`"
        elif name == "jobs_inline_in_dev" or name == "smtp_starttls":
            default_str = "`true`"

        desc = field.description or ""
        lines.append(f"| `{env_name}` | {default_str} | {desc} |")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check if README is up to date")
    args = parser.parse_args()

    table = generate_table()
    readme_content = README.read_text()

    if START_MARKER not in readme_content or END_MARKER not in readme_content:
        print("❌ Markers not found in README.md")
        return 1

    start_idx = readme_content.index(START_MARKER) + len(START_MARKER)
    end_idx = readme_content.index(END_MARKER)

    current_table = readme_content[start_idx:end_idx]

    if args.check:
        if current_table != table:
            print("❌ README.md environment variables table is out of date.")
            print("Run `uv run scripts/generate_env_docs.py` to update it.")
            return 1
        print("✅ README.md environment variables table is up to date.")
        return 0

    new_content = readme_content[:start_idx] + table + readme_content[end_idx:]
    README.write_text(new_content)
    print("✅ README.md environment variables table updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
