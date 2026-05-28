#!/usr/bin/env -S uv run python
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from h4ckath0n.config import Settings  # noqa: E402

README = REPO_ROOT / "README.md"


def generate_table():
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        if name == "env_prefix":
            continue
        if name == "openai_api_key":
            lines.append("| `OPENAI_API_KEY` | empty | OpenAI API key for the LLM wrapper |")
        env_name = f"H4CKATH0N_{name.upper()}"
        default_val = field.default
        if default_val == "":
            default_str = "empty"
        elif default_val == []:
            default_str = "`[]`"
        elif isinstance(default_val, bool):
            default_str = f"`{'true' if default_val else 'false'}`"
        else:
            default_str = f"`{default_val}`"

        desc = field.description or ""
        lines.append(f"| `{env_name}` | {default_str} | {desc} |")
    return "\n".join(lines)


def main():
    check_mode = "--check" in sys.argv
    readme_text = README.read_text()
    table = generate_table()

    start_marker = "<!-- GENERATED_ENV_VARS_START -->"
    end_marker = "<!-- GENERATED_ENV_VARS_END -->"

    pattern = re.compile(rf"({start_marker}\n).*?(\n{end_marker})", re.DOTALL)

    if not pattern.search(readme_text):
        print(f"❌ Could not find {start_marker} and {end_marker} in README.md")
        return 1

    new_readme = pattern.sub(rf"\g<1>{table}\g<2>", readme_text)

    if check_mode:
        if new_readme != readme_text:
            print(
                "❌ Environment variables documentation is out of date. "
                "Run `uv run scripts/generate_env_docs.py` to update."
            )
            return 1
        print("✅ Environment variables documentation is up to date.")
        return 0
    else:
        README.write_text(new_readme)
        print("✅ Updated environment variables documentation in README.md")
        return 0


if __name__ == "__main__":
    sys.exit(main())
