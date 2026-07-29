#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes via OpenAPI, generates a
Markdown table, and checks that README.md contains this exact table between
<!-- ROUTES_START --> and <!-- ROUTES_END --> markers.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI internal paths that we do not require in user docs.
FRAMEWORK_PATHS = frozenset({"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"})
HTTP_VERBS = frozenset({"get", "post", "put", "delete", "options", "head", "patch", "trace"})


def generate_route_table() -> str:
    """Return a Markdown table of (method, path) pairs from the live FastAPI app."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    routes: list[tuple[str, str, str]] = []
    paths = app.openapi()["paths"]
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, details in methods.items():
            if method.lower() not in HTTP_VERBS:
                continue
            if method.upper() == "HEAD":
                continue
            summary = details.get("summary", "")
            routes.append((path, method.upper(), summary))

    routes.sort(key=lambda x: (x[0], x[1]))

    lines = [
        "| Method | Path | Summary |",
        "|---|---|---|",
    ]
    for path, method, summary in routes:
        lines.append(f"| `{method}` | `{path}` | {summary} |")

    return "\n".join(lines)


def check_routes_in_readme(expected_table: str) -> bool:
    """Check if README.md contains the exact expected table between markers."""
    readme_text = README.read_text()

    pattern = re.compile(r"<!-- ROUTES_START -->\n(.*?)\n<!-- ROUTES_END -->", re.DOTALL)
    match = pattern.search(readme_text)
    if not match:
        print(
            "❌ Could not find <!-- ROUTES_START --> and <!-- ROUTES_END --> markers in README.md."
        )
        return False

    actual_table = match.group(1).strip()
    if actual_table != expected_table.strip():
        print("❌ API route documentation in README.md is out of sync with the app.")
        print("\nExpected table:\n")
        print(expected_table)
        return False

    return True


def main() -> int:
    expected_table = generate_route_table()
    if not check_routes_in_readme(expected_table):
        print("\nUpdate the section in README.md to match the expected table.")
        return 1

    print("✅ API routes are correctly documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
