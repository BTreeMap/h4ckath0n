#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes, and checks that
README.md mentions each one. Routes provided by FastAPI itself (e.g. /openapi.json,
/docs, /redoc) are excluded from the check.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI internal paths that we do not require in user docs.
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
    openapi_schema = app.openapi()
    paths = openapi_schema.get("paths", {})
    for path, path_item in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method in path_item:
            method_upper = method.upper()
            if method_upper == "HEAD":
                continue
            routes.append((method_upper, path))
    return sorted(routes)


def check_routes_in_readme(
    routes: list[tuple[str, str]],
) -> list[tuple[str, str]]:
    """Return routes that are not mentioned anywhere in README.md.

    We look for ``METHOD /path`` (e.g. ``GET /health``) so that sub-path
    matches like ``/auth/passkeys/{key_id}`` inside
    ``/auth/passkeys/{key_id}/revoke`` are not false positives.
    """
    readme_text = README.read_text()
    missing: list[tuple[str, str]] = []
    for method, path in routes:
        # Build a pattern like "GET /health" or "PATCH /auth/passkeys/\{key_id\}"
        # that must appear as a recognisable method+path token in the README.
        path_re = re.escape(path)
        combined = rf"`{method}\s+{path_re}`"
        if not re.search(combined, readme_text, re.IGNORECASE):
            missing.append((method, path))
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or fix API routes documentation in README.md."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically update the API routes in README.md.",
    )
    args = parser.parse_args()

    routes = get_app_routes()

    if args.fix:
        readme_text = README.read_text()

        # Generate the routes table or list
        from h4ckath0n.app import create_app
        from h4ckath0n.config import Settings

        app = create_app(
            Settings(
                database_url="sqlite+aiosqlite://",
                password_auth_enabled=True,
            )
        )
        paths = app.openapi().get("paths", {})

        routes_md_lines = []
        for method, path in routes:
            method_lower = method.lower()
            summary = paths.get(path, {}).get(method_lower, {}).get("summary", "")
            description = (
                paths.get(path, {}).get(method_lower, {}).get("description", "")
            )

            line = f"- `{method} {path}`"
            if summary:
                line += f" — {summary.lower()}"
                if not line.endswith("."):
                    line += "."
            if description and description.lower() != summary.lower():
                line += f" {description}"
            routes_md_lines.append(line)

        routes_md = "\n".join(routes_md_lines)

        # Replace everything between the markers
        pattern = re.compile(
            r"(<!-- BEGIN API ROUTES -->).*?(<!-- END API ROUTES -->)", re.DOTALL
        )
        if not pattern.search(readme_text):
            print(
                "❌ Could not find <!-- BEGIN API ROUTES --> and "
                "<!-- END API ROUTES --> markers in README.md."
            )
            return 1

        new_readme_text = pattern.sub(rf"\g<1>\n{routes_md}\n\g<2>", readme_text)
        README.write_text(new_readme_text)
        print("✅ Fixed API routes in README.md.")
        return 0

    missing = check_routes_in_readme(routes)

    if missing:
        print("❌ The following API routes are NOT documented in README.md:\n")
        for method, path in missing:
            print(f"  {method:6s} {path}")
        print(
            "\nAdd these routes to README.md or, if intentionally undocumented, "
            "add them to FRAMEWORK_PATHS in this script.\n"
            "Alternatively, run this script with --fix to automatically update README.md."
        )
        return 1

    print(f"✅ All {len(routes)} API routes are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
