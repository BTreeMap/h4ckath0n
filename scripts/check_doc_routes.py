#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the API routes table in README.md is up to date.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script generates a Markdown table of all API routes from the FastAPI OpenAPI schema
and ensures the README matches it exactly.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)

MARKER_START = "<!-- BEGIN_API_ROUTES -->"
MARKER_END = "<!-- END_API_ROUTES -->"


def generate_routes_table() -> str:
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    paths = app.openapi().get("paths", {})

    lines = ["| Method | Path | Summary |", "|---|---|---|"]

    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            if method.upper() == "HEAD":
                continue
            summary = op.get("summary", "")
            lines.append(f"| `{method.upper()}` | `{path}` | {summary} |")

    return "\n".join(lines)


def main() -> int:
    table = generate_routes_table()
    content = README.read_text()

    if MARKER_START not in content or MARKER_END not in content:
        print(f"Error: {MARKER_START} or {MARKER_END} not found in README.md")
        return 1

    pattern = re.compile(rf"{MARKER_START}.*?{MARKER_END}", re.DOTALL)

    match = pattern.search(content)
    if not match:
        print("Error: Could not find markers in README.md")
        return 1

    current_table = (
        match.group(0).replace(MARKER_START, "").replace(MARKER_END, "").strip()
    )

    if current_table == table:
        print("✅ API routes in README.md are up to date.")
        return 0

    if "--update" in sys.argv:
        new_content = pattern.sub(f"{MARKER_START}\n{table}\n{MARKER_END}", content)
        README.write_text(new_content)
        print("✅ Updated API routes in README.md.")
        return 0

    print("❌ API routes in README.md are out of date.")
    print("Run `uv run scripts/check_doc_routes.py --update` to fix.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
