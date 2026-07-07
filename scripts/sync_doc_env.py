#!/usr/bin/env -S uv run python
"""Drift-prevention script: sync the environment variables table in README.md.

Usage (from repo root):
    uv run scripts/sync_doc_env.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
GENERATOR = REPO_ROOT / "scripts" / "generate_doc_env.py"

START_MARKER = "<!-- BEGIN GENERATED ENV VARS -->"
END_MARKER = "<!-- END GENERATED ENV VARS -->"


def main() -> int:
    readme_text = README.read_text()

    # Run the generator
    result = subprocess.run(
        [sys.executable, str(GENERATOR)], capture_output=True, text=True, check=True
    )
    generated_content = result.stdout.strip()

    pattern = re.compile(rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL)

    if pattern.search(readme_text):
        # Update existing
        new_text = pattern.sub(generated_content, readme_text)
        if new_text != readme_text:
            README.write_text(new_text)
            print("✅ Updated README.md with latest env vars.")
        else:
            print("✅ README.md env vars are already up to date.")
    else:
        print(f"❌ Could not find {START_MARKER} in README.md")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
