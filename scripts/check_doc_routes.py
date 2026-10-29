#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py
    uv run scripts/check_doc_routes.py --update

The script imports the h4ckath0n app, enumerates all routes from the OpenAPI schema,
and checks that README.md mentions each one in a route table.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_openapi_routes() -> dict:
    """Return the OpenAPI paths dictionary."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    return app.openapi().get("paths", {})


def get_routes_list(paths: dict) -> list[tuple[str, str]]:
    """Flatten OpenAPI paths into a sorted list of (method, path) tuples."""
    routes: list[tuple[str, str]] = []
    for path, methods in paths.items():
        for method in methods:
            routes.append((method.upper(), path))
    return sorted(routes)


def check_routes_in_readme(
    routes: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """Return routes that are not mentioned in the README.md route table."""
    readme_text = README.read_text()
    missing: list[tuple[str, str]] = []
    for method, path in routes:
        path_re = re.escape(path)
        combined = rf"`{method}` \| `{path_re}`"
        if not re.search(combined, readme_text):
            missing.append((method, path))
    return missing


def update_readme(paths: dict) -> None:
    """Update the route table in README.md."""
    lines = [
        "<!-- route-table-start -->",
        "| Method | Path | Description |",
        "|---|---|---|",
    ]
    for path, methods in paths.items():
        for method, info in methods.items():
            summary = info.get("summary", "")
            lines.append(f"| `{method.upper()}` | `{path}` | {summary} |")
    lines.append("<!-- route-table-end -->")
    table = "\n".join(lines)

    text = README.read_text()
    if "<!-- route-table-start -->" not in text:
        print(
            "❌ Cannot update README.md: '<!-- route-table-start -->' marker not found."
        )
        sys.exit(1)

    new_text = re.sub(
        r"<!-- route-table-start -->.*<!-- route-table-end -->",
        table,
        text,
        flags=re.DOTALL,
    )
    README.write_text(new_text)
    print("✅ Updated route table in README.md.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or update API route documentation."
    )
    parser.add_argument(
        "--update", action="store_true", help="Update the README.md route table"
    )
    args = parser.parse_args()

    paths = get_openapi_routes()

    if args.update:
        update_readme(paths)
        return 0

    routes = get_routes_list(paths)
    missing = check_routes_in_readme(routes)

    if missing:
        print(
            "❌ The following API routes are NOT documented in README.md's route table:\n"
        )
        for method, path in missing:
            print(f"  {method:6s} {path}")
        print("\nRun this script with --update to regenerate the route table.")
        return 1

    print(f"✅ All {len(routes)} API routes are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
