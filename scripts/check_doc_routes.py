#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes, and checks that
README.md contains the generated markdown table of all routes.
Routes provided by FastAPI itself (e.g. /openapi.json,
/docs, /redoc) are excluded from the check.
"""

from __future__ import annotations

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

    # Use app.openapi() to reliably retrieve all registered endpoints and their metadata.
    paths = app.openapi().get("paths", {})
    for path, path_item in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, operation in path_item.items():
            if method.upper() == "HEAD":
                continue
            summary = operation.get("summary", "")
            routes.append((method.upper(), path, summary))
    return sorted(routes)


def generate_routes_table(routes: list[tuple[str, str, str]]) -> str:
    """Generate the markdown table for the routes."""
    lines = [
        "<!-- START GENERATED ROUTES -->",
        "| Method | Path | Summary |",
        "|---|---|---|",
    ]
    for method, path, summary in routes:
        lines.append(f"| `{method}` | `{path}` | {summary} |")
    lines.append("<!-- END GENERATED ROUTES -->")
    return "\n".join(lines)


def main() -> int:
    routes = get_app_routes()
    expected_table = generate_routes_table(routes)
    readme_text = README.read_text()

    if expected_table not in readme_text:
        print("❌ The API routes documented in README.md are out of date or missing.\n")
        print("Please replace the routes section in README.md with the following:\n")
        print(expected_table)
        print(
            "\nOr run `uv run scripts/update_doc_routes.py` to update it automatically."
        )
        return 1

    print(f"✅ All {len(routes)} API routes are documented correctly in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
