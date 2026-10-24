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
        for method, operation in path_item.items():
            summary = operation.get("summary", "")
            routes.append((method.upper(), path, summary))
    return sorted(routes)


def generate_routes_table(routes: list[tuple[str, str, str]]) -> str:
    """Generate a markdown table from the routes."""
    lines = ["| Method | Path | Summary |", "|---|---|---|"]
    for method, path, summary in routes:
        lines.append(f"| `{method}` | `{path}` | {summary} |")
    return "\n".join(lines)


def check_routes_in_readme(routes_table: str) -> bool:
    """Check if the exact generated table is in README.md."""
    readme_text = README.read_text()

    start_marker = "<!-- route-table-start -->"
    end_marker = "<!-- route-table-end -->"

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(
            "❌ Markers <!-- route-table-start --> and <!-- route-table-end --> not found."
        )
        return False

    current_table = readme_text[start_idx + len(start_marker) : end_idx].strip()
    return current_table == routes_table


def main() -> int:
    routes = get_app_routes()
    routes_table = generate_routes_table(routes)

    if "--update" in sys.argv:
        readme_text = README.read_text()
        start_marker = "<!-- route-table-start -->"
        end_marker = "<!-- route-table-end -->"
        new_text = re.sub(
            f"{start_marker}.*?{end_marker}",
            f"{start_marker}\\n{routes_table}\\n{end_marker}",
            readme_text,
            flags=re.DOTALL,
        )
        README.write_text(new_text)
        print("✅ README.md updated with latest API routes.")
        return 0

    is_matching = check_routes_in_readme(routes_table)

    if not is_matching:
        print("❌ The API routes in README.md are out of date or missing.")
        print("Run `uv run scripts/check_doc_routes.py --update` to fix it.")
        return 1

    print(f"✅ All {len(routes)} API routes are correctly documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
