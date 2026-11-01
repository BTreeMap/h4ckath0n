#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script imports the h4ckath0n app, enumerates all routes via OpenAPI, and checks that
README.md mentions each one. Routes provided by FastAPI itself are automatically
omitted by OpenAPI.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_app_routes() -> list[tuple[str, str, str]]:
    """Return (method, path, summary) tuples from the live FastAPI app."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    paths = app.openapi().get("paths", {})

    routes: list[tuple[str, str, str]] = []
    for path, methods in paths.items():
        for method, op in methods.items():
            routes.append((method.upper(), path, op.get("summary", "")))
    return sorted(routes)


def check_routes_in_readme(
    routes: list[tuple[str, str, str]],
) -> list[tuple[str, str]]:
    """Return routes that are not mentioned anywhere in README.md.

    We look for ``| `METHOD` | `/path` |`` so that sub-path
    matches are not false positives and we explicitly match table columns.
    """
    readme_text = README.read_text()
    missing: list[tuple[str, str]] = []
    for method, path, _ in routes:
        # Match exact table column formatting.
        path_re = re.escape(path)
        combined = rf"`{method}`\s*\|\s*`{path_re}`"
        if not re.search(combined, readme_text, re.IGNORECASE):
            missing.append((method, path))
    return missing


def generate_route_table(routes: list[tuple[str, str, str]]) -> str:
    """Generate the markdown table for routes."""
    lines = [
        "| Method | Route | Description |",
        "|---|---|---|",
    ]
    for method, path, summary in routes:
        lines.append(f"| `{method}` | `{path}` | {summary} |")
    return "\n".join(lines)


def update_readme(routes: list[tuple[str, str, str]]) -> bool:
    """Update README.md with the generated table. Returns True if modified."""
    readme_text = README.read_text()
    start_marker = "<!-- route-table-start -->"
    end_marker = "<!-- route-table-end -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print(f"❌ {start_marker} or {end_marker} not found in README.md")
        sys.exit(1)

    expected_table = generate_route_table(routes)

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker) + len(end_marker)

    before = readme_text[:start_idx]
    after = readme_text[end_idx:]

    new_text = f"{before}{start_marker}\n\n{expected_table}\n\n{end_marker}{after}"

    if new_text != readme_text:
        README.write_text(new_text)
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update", action="store_true", help="Update the README.md file in place"
    )
    args = parser.parse_args()
    routes = get_app_routes()

    if args.update:
        changed = update_readme(routes)
        if changed:
            print("✅ Updated API routes table in README.md.")
        else:
            print("✅ API routes table in README.md is already up to date.")
        return 0

    missing = check_routes_in_readme(routes)

    if missing:
        print("❌ The following API routes are NOT documented in README.md:\n")
        for method, path in missing:
            print(f"  {method:6s} {path}")
        print("\nRun `uv run scripts/check_doc_routes.py --update` to fix.")
        return 1

    print(f"✅ All {len(routes)} API routes are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
