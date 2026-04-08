#!/usr/bin/env python3
import sys

from h4ckath0n.config import Settings

BEGIN_MARKER = "<!-- BEGIN ENV VARS -->"
END_MARKER = "<!-- END ENV VARS -->"


def generate_table() -> str:
    lines = ["| Variable | Default | Description |", "|---|---|---|"]
    for name, field in Settings.model_fields.items():
        if name == "model_config":
            continue

        var_name = f"H4CKATH0N_{name.upper()}"
        default = field.default if not field.is_required() else "empty"

        if default == "" or default == "empty":
            default_str = "empty"
        elif default is False:
            default_str = "`false`"
        elif default is True:
            default_str = "`true`"
        elif default == []:
            default_str = "`[]`"
        else:
            default_str = f"`{default}`"

        desc = field.description or ""

        if name == "openai_api_key":
            lines.append(f"| `OPENAI_API_KEY` | empty | {desc} |")
            lines.append(f"| `H4CKATH0N_OPENAI_API_KEY` | empty | Alternate {desc} |")
        else:
            lines.append(f"| `{var_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main():
    update = "--update" in sys.argv
    table_content = generate_table()

    with open("README.md") as f:
        readme = f.read()

    if BEGIN_MARKER not in readme or END_MARKER not in readme:
        print("Markers not found in README.md")
        sys.exit(1)

    start_idx = readme.find(BEGIN_MARKER) + len(BEGIN_MARKER)
    end_idx = readme.find(END_MARKER)

    current_content = readme[start_idx:end_idx].strip()

    if current_content == table_content:
        print("✅ Environment variables documentation is up to date.")
        sys.exit(0)

    if update:
        new_readme = readme[:start_idx] + "\n" + table_content + "\n" + readme[end_idx:]
        with open("README.md", "w") as f:
            f.write(new_readme)
        print("✅ Updated README.md with latest environment variables.")
    else:
        print(
            "❌ Environment variables documentation is out of date. "
            "Run `uv run --locked scripts/check_doc_env_vars.py --update` to fix."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
