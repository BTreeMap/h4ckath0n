#!/usr/bin/env -S uv run python
"""Drift-prevention generation: update docs/configuration/index.md with all env vars.

Usage (from repo root):
    uv run scripts/generate_config_docs.py
"""

import re
import sys
from pathlib import Path


def main() -> int:
    from h4ckath0n.config import Settings

    lines = []
    lines.append("| Environment Variable | Type | Default |")
    lines.append("| --- | --- | --- |")

    for name, field_info in Settings.model_fields.items():
        env_var = f"H4CKATH0N_{name.upper()}"

        # Determine type
        ann = str(field_info.annotation)
        if "str" in ann:
            t = "string"
        elif "int" in ann:
            t = "integer"
        elif "bool" in ann:
            t = "boolean"
        elif "list" in ann:
            t = "list"
        else:
            t = ann

        # Determine default
        default = field_info.default
        if default == "" or default == []:
            default_str = f"`{repr(default)}`"
        elif default is not None:
            default_str = f"`{default}`"
        else:
            default_str = "None"

        lines.append(f"| `{env_var}` | {t} | {default_str} |")

    table = "\n".join(lines)

    docs_file = Path("docs/configuration/index.md")
    content = docs_file.read_text()

    new_content = re.sub(
        r"<!-- ENV_VARS_START -->.*?<!-- ENV_VARS_END -->",
        f"<!-- ENV_VARS_START -->\n{table}\n<!-- ENV_VARS_END -->",
        content,
        flags=re.DOTALL,
    )

    docs_file.write_text(new_content)
    print("✅ docs/configuration/index.md updated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
