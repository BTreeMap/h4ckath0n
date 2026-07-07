#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the configuration env vars in README.md are up to date.

Usage (from repo root):
    uv run scripts/check_doc_env.py
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

    match = pattern.search(readme_text)
    if not match:
        print(f"❌ Could not find {START_MARKER} in README.md")
        return 1

    current_content = match.group(0)

    if current_content != generated_content:
        print(
            "❌ Env vars in README.md are out of date. Run `uv run scripts/sync_doc_env.py` "
            "to fix."
        )
        return 1

    print("✅ Env vars in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
