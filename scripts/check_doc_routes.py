#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes, and checks that
README.md mentions each one. Routes provided by FastAPI itself (e.g. /openapi.json,
/docs, /redoc) are excluded from the check.
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


def get_app_routes() -> list[tuple[str, str]]:
    """Return (method, path) pairs from the live FastAPI app's OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    routes: list[tuple[str, str]] = []
    paths = app.openapi().get("paths", {})
    for path, path_item in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method in path_item:
            routes.append((method.upper(), path))
    return sorted(routes)


def check_routes_in_readme(
    routes: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """Return routes that are not mentioned anywhere in README.md.

    We look for ``| `METHOD` | `/path` |`` in the generated route table.
    """
    readme_text = README.read_text()

    # Try to extract the table first
    table_match = re.search(
        r"<!-- route-table-start -->(.*?)<!-- route-table-end -->",
        readme_text,
        re.DOTALL,
    )

    search_text = table_match.group(1) if table_match else readme_text

    missing: list[tuple[str, str]] = []
    for method, path in routes:
        path_re = re.escape(path)
        # Match exactly the table format to avoid substring matches
        combined = rf"`{method}`\s*\|\s*`{path_re}`"
        if not re.search(combined, search_text, re.IGNORECASE):
            missing.append((method, path))
    return missing


def main() -> int:
    routes = get_app_routes()
    missing = check_routes_in_readme(routes)

    if missing:
        print("❌ The following API routes are NOT documented in README.md:\n")
        for method, path in missing:
            print(f"  {method:6s} {path}")
        print(
            "\nAdd these routes to README.md or, if intentionally undocumented, "
            "add them to FRAMEWORK_PATHS in this script."
        )
        return 1

    print(f"✅ All {len(routes)} API routes are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
