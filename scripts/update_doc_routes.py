#!/usr/bin/env -S uv run python
"""Update the README.md with the generated API routes table.

Usage (from repo root):
    uv run scripts/update_doc_routes.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
CHECK_SCRIPT = REPO_ROOT / "scripts" / "check_doc_routes.py"


def main() -> int:
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_doc_routes", CHECK_SCRIPT)
    if spec is None or spec.loader is None:
        print("Failed to load check_doc_routes.py")
        return 1

    check_doc_routes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check_doc_routes)

    routes = check_doc_routes.get_app_routes()
    expected_table = check_doc_routes.generate_routes_table(routes)

    readme_text = README.read_text()

    # Pattern to match the existing routes section, or the generated block if it exists
    generated_pattern = re.compile(
        r"<!-- START GENERATED ROUTES -->.*?<!-- END GENERATED ROUTES -->", re.DOTALL
    )

    if generated_pattern.search(readme_text):
        new_text = generated_pattern.sub(expected_table, readme_text)
    else:
        print("Could not find generated routes block to replace.")
        return 1

    if new_text != readme_text:
        README.write_text(new_text)
        print("✅ README.md updated with latest API routes.")
    else:
        print("✅ README.md is already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
