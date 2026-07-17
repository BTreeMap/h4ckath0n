#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the API routes in the FastAPI app match README.md.

Usage (from repo root):
    uv run scripts/check_doc_routes.py
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    generator = REPO_ROOT / "scripts" / "generate_doc_routes.py"
    result = subprocess.run(
        [sys.executable, str(generator), "--check"], capture_output=True, text=True
    )
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
