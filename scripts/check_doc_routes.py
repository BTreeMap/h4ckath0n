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

# FastAPI internal paths that we do not require in user docs.
FRAMEWORK_PATHS = frozenset({"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"})


def get_openapi_routes() -> str:
    """Return a markdown list of endpoints from the OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    paths = app.openapi()["paths"]

    routes_by_tag: dict[str, list[tuple[str, str, str]]] = {}
    for path, path_item in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, info in path_item.items():
            if method.upper() == "HEAD":
                continue
            tags = info.get("tags", ["default"])
            tag = tags[0] if tags else "default"
            if tag not in routes_by_tag:
                routes_by_tag[tag] = []
            routes_by_tag[tag].append((method.upper(), path, info.get("summary", "")))

    # Print markdown
    lines = []
    for tag in sorted(routes_by_tag.keys()):
        lines.append(f"### {tag.title()}")
        for method, path, summary in routes_by_tag[tag]:
            lines.append(f"- `{method} {path}` — {summary}")
        lines.append("")
    return "\n".join(lines).strip()


def check_routes_in_readme(expected_markdown: str, update: bool = False) -> int:
    """Verify or update the API routes block in README.md."""
    readme_text = README.read_text()

    pattern = re.compile(r"(<!-- BEGIN_API_ROUTES -->\n)(.*?)(<!-- END_API_ROUTES -->)", re.DOTALL)

    match = pattern.search(readme_text)
    if not match:
        print("❌ Could not find BEGIN_API_ROUTES and END_API_ROUTES markers in README.md.")
        return 1

    current_markdown = match.group(2).strip()

    if current_markdown == expected_markdown:
        print("✅ API routes in README.md are up to date.")
        return 0

    if update:
        new_text = pattern.sub(rf"\1{expected_markdown}\3", readme_text)
        README.write_text(new_text)
        print("✅ Updated API routes in README.md.")
        return 0

    print("❌ API routes in README.md are out of date.\n")
    print("Expected:")
    print(expected_markdown)
    print("\nRun with --update to fix.")
    return 1


def main() -> int:
    update = "--update" in sys.argv
    expected_markdown = get_openapi_routes()
    return check_routes_in_readme(expected_markdown, update=update)


if __name__ == "__main__":
    sys.exit(main())
