#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that README.md configuration table matches config.py.

Usage:
    uv run scripts/generate_doc_config.py [--check]
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- CONFIG_TABLE_START -->"
END_MARKER = "<!-- CONFIG_TABLE_END -->"


def generate_table() -> str:
    from h4ckath0n.config import Settings  # noqa: E402

    lines = [
        "| Variable | Default | Description |",
        "|---|---|---|",
    ]

    for field_name, field_info in Settings.model_fields.items():
        var_name = f"H4CKATH0N_{field_name.upper()}"

        if field_info.is_required():
            default_str = "required"
        elif (
            field_info.default is not None
            and getattr(field_info.default, "__name__", "") != "PydanticUndefined"
        ):
            if isinstance(field_info.default, bool):
                default_str = f"`{'true' if field_info.default else 'false'}`"
            elif isinstance(field_info.default, list) and len(field_info.default) == 0:
                default_str = "`[]`"
            elif field_info.default == "":
                default_str = "empty"
            elif field_name == "database_url":
                default_str = "`sqlite:///./h4ckath0n.db`"
            elif field_name == "origin":
                default_str = "`http://localhost:8000` in development"
            elif field_name == "rp_id":
                default_str = "`localhost` in development"
            elif str(field_info.default) == "PydanticUndefined":
                if field_info.default_factory is not None:
                    default_str = "`[]`" if field_info.default_factory is list else "empty"
                else:
                    default_str = "empty"
            else:
                default_str = f"`{field_info.default}`"
        elif field_info.default_factory is not None:
            default_str = "`[]`" if field_info.default_factory is list else "empty"
        else:
            default_str = "empty"

        desc = field_info.description or ""
        lines.append(f"| `{var_name}` | {default_str} | {desc} |")

    return "\n".join(lines)


def main() -> int:
    check_mode = "--check" in sys.argv
    table = generate_table()

    readme_text = README.read_text()

    start_idx = readme_text.find(START_MARKER)
    end_idx = readme_text.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print("❌ Markers not found in README.md")
        return 1

    before = readme_text[: start_idx + len(START_MARKER)]
    after = readme_text[end_idx:]

    new_text = f"{before}\n{table}\n{after}"

    if check_mode:
        if readme_text != new_text:
            print(
                "❌ README.md configuration table is out of sync. "
                "Run scripts/generate_doc_config.py to update."
            )
            return 1
        print("✅ README.md configuration table is up to date.")
        return 0
    else:
        README.write_text(new_text)
        print("✅ Updated README.md configuration table.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
