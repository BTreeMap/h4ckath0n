#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes via OpenAPI, and injects
the documentation into README.md between <!-- API_ROUTES_START --> and
<!-- API_ROUTES_END -->. It fails if the file needs to be updated (drift detection).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
FRAMEWORK_PATHS = frozenset({"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"})


def get_openapi_routes() -> list[tuple[str, str, str, str]]:
    """Return (tag, method, path, description) from the live FastAPI app."""
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    openapi_schema = app.openapi()

    routes = []
    for path, path_item in openapi_schema.get("paths", {}).items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, operation in path_item.items():
            tag = operation.get("tags", ["default"])[0]
            summary = operation.get("summary", "")
            desc = operation.get("description", "")
            full_desc = f"{summary}. {desc}".strip(" .") + "."
            routes.append((tag, method.upper(), path, full_desc))

    # Sort by tag then path
    routes.sort(key=lambda r: (r[0], r[2], r[1]))
    return routes


def generate_markdown(routes: list[tuple[str, str, str, str]]) -> str:
    lines = ["<!-- API_ROUTES_START -->\n"]
    current_tag = None
    for tag, method, path, desc in routes:
        if tag != current_tag:
            lines.append(f"\n### {tag.title().replace('-', ' ')}\n\n")
            current_tag = tag
        lines.append(f"- `{method} {path}` — {desc}\n")
    lines.append("\n<!-- API_ROUTES_END -->")
    return "".join(lines)


def main() -> int:
    routes = get_openapi_routes()
    new_block = generate_markdown(routes)

    readme_text = README.read_text()
    pattern = re.compile(r"<!-- API_ROUTES_START -->.*?<!-- API_ROUTES_END -->", re.DOTALL)

    if not pattern.search(readme_text):
        print("❌ Could not find API_ROUTES markers in README.md")
        return 1

    updated_text = pattern.sub(new_block, readme_text)

    if updated_text != readme_text:
        README.write_text(updated_text)
        print("❌ README.md was out of date. It has been updated automatically.")
        print("Please review and commit the changes.")
        return 1

    print(f"✅ All {len(routes)} API routes are documented and up to date in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
