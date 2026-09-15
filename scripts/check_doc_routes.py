#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, generates the OpenAPI spec, and checks that
README.md contains the exact generated markdown table inside HTML comments.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from h4ckath0n.app import create_app
from h4ckath0n.config import Settings

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_expected_routes_markdown() -> str:
    """Return the expected markdown table of routes from the OpenAPI spec."""
    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    paths = app.openapi().get("paths", {})

    lines = [
        "| Method | Path | Summary |",
        "|--------|------|---------|",
    ]
    for path, methods in paths.items():
        for method, op in methods.items():
            summary = op.get("summary", "")
            lines.append(f"| `{method.upper()}` | `{path}` | {summary} |")
    return "\n" + "\n".join(lines) + "\n"


def main() -> int:
    readme_text = README.read_text()
    match = re.search(
        r"<!-- BEGIN ROUTES -->(.*?)<!-- END ROUTES -->", readme_text, re.DOTALL
    )

    if not match:
        print(
            "❌ <!-- BEGIN ROUTES --> and <!-- END ROUTES --> markers not found in README.md."
        )
        return 1

    expected_block = get_expected_routes_markdown()
    actual_block = match.group(1)

    if actual_block != expected_block:
        print("❌ API routes in README.md are out of sync with the application.\n")
        print("Expected block to look like:")
        print(expected_block)
        print(
            "Please update the table inside <!-- BEGIN ROUTES --> ... <!-- END ROUTES -->."
        )
        return 1

    print("✅ API routes in README.md perfectly match the OpenAPI spec.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
