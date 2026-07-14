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
    openapi_schema = app.openapi()
    paths = openapi_schema.get("paths", {})
    http_methods = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            if method.lower() in http_methods:
                summary = op.get("summary", "")
                routes.append((method.upper(), path, summary))
    return sorted(routes)


def generate_routes_table(routes: list[tuple[str, str, str]]) -> str:
    """Format the routes into a Markdown table."""
    lines = ["| Method | Path | Description |", "|---|---|---|"]
    for method, path, summary in routes:
        lines.append(f"| `{method}` | `{path}` | {summary} |")
    return "\n".join(lines)


def update_readme(check_only: bool = False) -> int:
    routes = get_app_routes()
    table = generate_routes_table(routes)
    readme_text = README.read_text()

    pattern = r"(<!-- BEGIN API ROUTES -->).*?(<!-- END API ROUTES -->)"
    replacement = rf"\1\n\n{table}\n\n\2"

    new_text, count = re.subn(pattern, replacement, readme_text, flags=re.DOTALL)
    if count == 0:
        print("❌ Could not find API ROUTES markers in README.md")
        return 1

    if new_text != readme_text:
        if check_only:
            print(
                "❌ README.md API routes are out of date. "
                "Run scripts/check_doc_routes.py --update to fix."
            )
            return 1
        README.write_text(new_text)
        print("✅ Updated API routes in README.md")
    else:
        print(f"✅ All {len(routes)} API routes are correctly documented in README.md.")
    return 0


def main() -> int:
    check_only = "--update" not in sys.argv
    return update_readme(check_only)


if __name__ == "__main__":
    sys.exit(main())
