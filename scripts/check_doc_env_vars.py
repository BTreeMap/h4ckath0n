#!/usr/bin/env python3
import argparse
import re
import sys

from h4ckath0n.config import Settings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    table_lines = ["| Variable | Default | Description |", "|---|---|---|"]

    for name, field in Settings.model_fields.items():
        if name == "model_config":
            continue

        env_var = f"H4CKATH0N_{name.upper()}"
        if name == "openai_api_key":
            env_var = "`OPENAI_API_KEY` or `H4CKATH0N_OPENAI_API_KEY`"
        else:
            env_var = f"`{env_var}`"

        default = field.default_factory() if field.default_factory is not None else field.default

        if default == "" or default == []:
            default_str = "empty"
        elif isinstance(default, bool):
            default_str = f"`{'true' if default else 'false'}`"
        elif name == "rp_id":
            default_str = "`localhost` in development"
        elif name == "origin":
            default_str = "`http://localhost:8000` in development"
        else:
            default_str = f"`{default}`"

        desc = field.description or ""
        table_lines.append(f"| {env_var} | {default_str} | {desc} |")

    table_str = "\n".join(table_lines)
    full_str = f"<!-- BEGIN ENV VARS -->\n{table_str}\n<!-- END ENV VARS -->"

    with open("README.md") as f:
        readme = f.read()

    pattern = re.compile(r"<!-- BEGIN ENV VARS -->.*?<!-- END ENV VARS -->", re.DOTALL)

    if "<!-- BEGIN ENV VARS -->" not in readme:
        print("Error: Markers not found in README.md")
        sys.exit(1)

    current_match = pattern.search(readme)
    if current_match.group(0) == full_str:
        print("✅ Environment variables documentation is up to date.")
        sys.exit(0)

    if args.update:
        new_readme = pattern.sub(full_str, readme)
        with open("README.md", "w") as f:
            f.write(new_readme)
        print("✅ README.md updated with environment variables.")
        sys.exit(0)
    else:
        print("❌ Environment variables documentation is out of date. Run with --update.")
        sys.exit(1)


if __name__ == "__main__":
    main()
