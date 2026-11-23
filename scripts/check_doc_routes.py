#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script imports the h4ckath0n app, enumerates all routes, and checks that
README.md mentions each one in the route table.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


def get_app_routes() -> list[tuple[str, str, str]]:
    """Return (method, path, summary) tuples from the OpenAPI schema."""
    os.environ["H4CKATH0N_PASSWORD_AUTH_ENABLED"] = "true"

    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    schema = app.openapi()
    routes: list[tuple[str, str, str]] = []

    for path, methods in schema.get("paths", {}).items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            routes.append((method.upper(), path, op.get("summary", "")))

    routes.sort(key=lambda r: (r[1], r[0]))
    return routes


def check_routes_in_readme(routes: list[tuple[str, str, str]]) -> list[tuple[str, str]]:
    readme_text = README.read_text()
    missing: list[tuple[str, str]] = []
    for method, path, _ in routes:
        path_re = re.escape(path)
        combined = rf"`{method}` \| `{path_re}`"
        if not re.search(combined, readme_text, re.IGNORECASE):
            missing.append((method, path))
    return missing


def update_readme(routes: list[tuple[str, str, str]]) -> None:
    readme_text = README.read_text()

    table_lines = [
        "<!-- route-table-start -->",
        "| Method | Path | Summary |",
        "|---|---|---|",
    ]
    for method, path, summary in routes:
        table_lines.append(f"| `{method}` | `{path}` | {summary} |")
    table_lines.append("<!-- route-table-end -->")

    table_str = "\n".join(table_lines)

    pattern = re.compile(
        r"<!-- route-table-start -->.*<!-- route-table-end -->", re.DOTALL
    )
    if pattern.search(readme_text):
        new_text = pattern.sub(table_str, readme_text)
        README.write_text(new_text)
        print("✅ Updated route table in README.md.")
    else:
        print(
            "❌ Could not find <!-- route-table-start --> markers in README.md.",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update the README table")
    args = parser.parse_args()

    routes = get_app_routes()

    if args.update:
        update_readme(routes)
        return 0

    missing = check_routes_in_readme(routes)

    if missing:
        print("❌ The following API routes are NOT documented in README.md:\n")
        for method, path in missing:
            print(f"  {method:6s} {path}")
        print(
            "\nAdd these routes to the table in README.md or update the table using --update."
        )
        return 1

    print(f"✅ All {len(routes)} API routes are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
