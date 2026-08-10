#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--fix]

The script imports the h4ckath0n app, generates the OpenAPI schema, and checks that
README.md contains the exact API routes section. Use --fix to rewrite README.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI internal paths that we do not require in user docs.
FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


def get_app_routes() -> list[tuple[str, str, str]]:
    """Return (method, path, summary) from the live FastAPI app's OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    paths = app.openapi().get("paths", {})
    routes: list[tuple[str, str, str]] = []

    for path, ops in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in ops.items():
            method_upper = method.upper()
            if method_upper == "HEAD":
                continue
            summary = op.get("summary", "")
            routes.append((method_upper, path, summary))

    # Sort by path first, then method
    return sorted(routes, key=lambda x: (x[1], x[0]))


def generate_routes_markdown(routes: list[tuple[str, str, str]]) -> str:
    lines = []
    for method, path, summary in routes:
        desc = f" — {summary}" if summary else ""
        lines.append(f"- `{method} {path}`{desc}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or fix API routes in README.md")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Fix README.md by updating the API routes section",
    )
    args = parser.parse_args()

    routes = get_app_routes()
    routes_md = generate_routes_markdown(routes)

    readme_text = README.read_text()

    start_marker = "<!-- BEGIN API ROUTES -->\n"
    end_marker = "<!-- END API ROUTES -->\n"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Structural markers not found in README.md")
        return 1

    start_idx = readme_text.find(start_marker) + len(start_marker)
    end_idx = readme_text.find(end_marker)

    current_section = readme_text[start_idx:end_idx]

    if current_section == routes_md:
        print(f"✅ All {len(routes)} API routes are correctly documented in README.md.")
        return 0

    if args.fix:
        new_readme_text = readme_text[:start_idx] + routes_md + readme_text[end_idx:]
        README.write_text(new_readme_text)
        print(f"✅ Updated README.md with {len(routes)} API routes.")
        return 0
    else:
        print("❌ API routes in README.md are out of date or incorrectly formatted.")
        print("Run `uv run scripts/check_doc_routes.py --fix` to update it.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
