#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that API routes are documented via a generated table.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes via OpenAPI, and checks that
README.md contains the exact generated table.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI paths omitted from user docs.
FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


def get_app_routes() -> list[tuple[str, str, str]]:
    """Return (method, path, summary) tuples from the live FastAPI app."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    routes: list[tuple[str, str, str]] = []

    paths = app.openapi().get("paths", {})
    for path, path_item in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in path_item.items():
            method = method.upper()
            if method == "HEAD":
                continue
            summary = op.get("summary", "")
            routes.append((method, path, summary))
    return sorted(routes)


def generate_table(routes: list[tuple[str, str, str]]) -> str:
    lines = []
    lines.append("<!-- BEGIN ROUTES -->")
    lines.append("| Method | Path | Description |")
    lines.append("|---|---|---|")
    for method, path, summary in routes:
        lines.append(f"| `{method}` | `{path}` | {summary} |")
    lines.append("<!-- END ROUTES -->")
    return "\n".join(lines)


def main() -> int:
    routes = get_app_routes()
    expected_table = generate_table(routes)

    readme_text = README.read_text()

    # Extract existing table from README
    match = re.search(
        r"<!-- BEGIN ROUTES -->.*?<!-- END ROUTES -->", readme_text, flags=re.DOTALL
    )
    if not match:
        print("❌ Could not find `<!-- BEGIN ROUTES -->` markers in README.md.")
        return 1

    actual_table = match.group(0)
    if actual_table != expected_table:
        print("❌ API routes in README.md are out of date.\n")
        print("Please replace the table in README.md with the latest routes.")
        print("Expected:\n")
        print(expected_table)
        return 1

    print(f"✅ All {len(routes)} API routes are correctly documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
