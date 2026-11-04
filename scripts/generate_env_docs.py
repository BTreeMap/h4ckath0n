#!/usr/bin/env -S uv run python
"""Generate the environment variables table in README.md from the Settings model."""

import sys
from pathlib import Path

from check_doc_env import generate_env_table

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def main():
    readme_text = README.read_text()
    expected_table = generate_env_table()

    start_marker = "All settings use the `H4CKATH0N_` prefix unless noted.\n\n"
    end_marker = "\n\nIn development, missing `RP_ID`"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Could not find configuration table boundaries in README.md")
        sys.exit(1)

    start_idx = readme_text.index(start_marker) + len(start_marker)
    end_idx = readme_text.index(end_marker)

    new_readme = readme_text[:start_idx] + expected_table + readme_text[end_idx:]
    README.write_text(new_readme)
    print(
        "✅ Successfully updated README.md with generated environment variables table."
    )


if __name__ == "__main__":
    main()
