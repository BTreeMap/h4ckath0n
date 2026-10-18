#!/usr/bin/env -S uv run python
"""Verify that the environment variable documentation is up to date."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
ENV_EXAMPLE = REPO_ROOT / ".env.example"


def main() -> int:
    sys.path.insert(0, str(REPO_ROOT))
    from scripts.generate_doc_env import generate_env_example, generate_env_table

    expected_table = generate_env_table()
    content = README.read_text()

    start_marker = "<!-- ENV_START -->\n"
    end_marker = "<!-- ENV_END -->\n"

    if start_marker not in content or end_marker not in content:
        print("❌ Missing ENV_START or ENV_END markers in README.md")
        return 1

    actual_table = content.split(start_marker)[1].split(end_marker)[0]
    if expected_table != actual_table:
        print("❌ Environment variables in README.md are out of date.")
        print("Run `uv run scripts/generate_doc_env.py` to update.")
        return 1

    expected_example = generate_env_example()
    if not ENV_EXAMPLE.exists():
        print("❌ .env.example is missing.")
        print("Run `uv run scripts/generate_doc_env.py` to create it.")
        return 1

    if ENV_EXAMPLE.read_text() != expected_example:
        print("❌ .env.example is out of date.")
        print("Run `uv run scripts/generate_doc_env.py` to update.")
        return 1

    print("✅ Environment variables documentation is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
