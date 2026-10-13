#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every ``Settings`` environment variable is documented."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
ENV_EXAMPLE = REPO_ROOT / ".env.example"


def get_settings_info() -> list[tuple[str, str, str]]:
    from h4ckath0n.config import Settings

    info = []
    # openai_api_key has custom resolution in h4ckath0n
    for name, field in Settings.model_fields.items():
        if name == "openai_api_key":
            info.append(("OPENAI_API_KEY", "empty", field.description or ""))
            info.append(
                (
                    "H4CKATH0N_OPENAI_API_KEY",
                    "empty",
                    "Alternate OpenAI API key for the LLM wrapper",
                )
            )
            continue

        env_name = f"H4CKATH0N_{name.upper()}"
        default = field.default
        if default == "":
            default_str = "empty"
        elif isinstance(default, list) or getattr(field, "default_factory", None):
            default_str = "`[]`"
        elif isinstance(default, bool):
            default_str = f"`{'true' if default else 'false'}`"
        else:
            default_str = f"`{default}`"

        desc = field.description or ""
        info.append((env_name, default_str, desc))
    return info


def generate_markdown_table(info: list[tuple[str, str, str]]) -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for env_name, default_str, desc in info:
        lines.append(f"| `{env_name}` | {default_str} | {desc} |")
    return "\n".join(lines) + "\n"


def generate_env_example(info: list[tuple[str, str, str]]) -> str:
    lines = ["# Auto-generated from h4ckath0n.config.Settings"]
    for env_name, _, desc in info:
        if desc:
            lines.append(f"# {desc}")
        lines.append(f"{env_name}=")
        lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true", help="Update docs in place")
    args = parser.parse_args()

    info = get_settings_info()
    expected_table = generate_markdown_table(info)
    expected_env = generate_env_example(info)

    readme_text = README.read_text()

    start_marker = "<!-- START_ENV -->\n"
    end_marker = "<!-- END_ENV -->\n"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Missing <!-- START_ENV --> or <!-- END_ENV --> markers in README.md")
        return 1

    pattern = re.compile(
        rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL
    )
    current_table_match = pattern.search(readme_text)
    if not current_table_match:
        print("❌ Could not find content between markers in README.md")
        return 1

    expected_content = f"{start_marker}{expected_table}{end_marker}"

    readme_matches = current_table_match.group(0) == expected_content
    env_matches = ENV_EXAMPLE.exists() and ENV_EXAMPLE.read_text() == expected_env

    if readme_matches and env_matches:
        print("✅ Environment documentation and .env.example are up to date.")
        return 0

    if args.fix:
        new_readme = pattern.sub(expected_content, readme_text)
        README.write_text(new_readme)
        ENV_EXAMPLE.write_text(expected_env)
        print("🔧 Fixed README.md and .env.example")
        return 0
    else:
        print(
            "❌ Documentation is out of date. Run `uv run scripts/check_doc_env.py --fix` to update."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
