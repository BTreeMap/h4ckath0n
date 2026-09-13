#!/usr/bin/env -S uv run python
"""Drift-prevention script: generates API route documentation for README.md from the FastAPI app."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
CHECK_SCRIPT = REPO_ROOT / "scripts" / "check_doc_routes.py"


def main() -> int:
    import check_doc_routes

    readme_text = check_doc_routes.README.read_text(encoding="utf-8")
    start_marker = "<!-- BEGIN ROUTES -->"
    end_marker = "<!-- END ROUTES -->"

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("❌ Error: README.md is missing route markers.", file=sys.stderr)
        return 1

    prefix = readme_text[: start_idx + len(start_marker)]
    suffix = readme_text[end_idx:]

    expected_content = "\n" + check_doc_routes.get_app_routes_markdown() + "\n"
    expected_readme = prefix + expected_content + suffix

    if readme_text != expected_readme:
        README.write_text(expected_readme, encoding="utf-8")
        print("✅ Updated API routes in README.md.")
    else:
        print("✅ API routes in README.md are already up to date.")

    return 0


if __name__ == "__main__":
    # Ensure scripts directory is in path to import check_doc_routes
    sys.path.insert(0, str(CHECK_SCRIPT.parent))
    sys.exit(main())
