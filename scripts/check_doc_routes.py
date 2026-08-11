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


def get_app_routes_from_openapi() -> list[tuple[str, str, str]]:
    """Return (method, path, summary) from the live FastAPI app's OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    openapi = app.openapi()

    routes: list[tuple[str, str, str]] = []
    for path, methods in openapi.get("paths", {}).items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            summary = op.get("summary", "")
            routes.append((method.upper(), path, summary))
    return routes


def check_routes_in_readme(
    routes: list[tuple[str, str, str]],
) -> bool:
    """Check if the API routes table in README matches the generated table."""
    readme_text = README.read_text()
    expected_block = generate_routes_block(routes)

    pattern = r"(<!-- BEGIN API ROUTES -->).*?(<!-- END API ROUTES -->)"
    match = re.search(pattern, readme_text, flags=re.DOTALL)
    if not match:
        print("❌ Could not find <!-- BEGIN API ROUTES --> markers in README.md")
        return False

    actual_block = match.group(0)
    return actual_block.strip() == expected_block.strip()


def generate_routes_block(routes: list[tuple[str, str, str]]) -> str:
    """Generate the markdown block for routes."""
    lines = [
        "<!-- BEGIN API ROUTES -->",
        "",
        "| Method | Path | Summary |",
        "|---|---|---|",
    ]
    for method, path, summary in routes:
        lines.append(f"| `{method}` | `{path}` | {summary} |")
    lines.extend(["", "<!-- END API ROUTES -->"])
    return "\n".join(lines)


def fix_readme(routes: list[tuple[str, str, str]]) -> None:
    """Rewrite the README to insert the correct routes block."""
    readme_text = README.read_text()
    expected_block = generate_routes_block(routes)

    pattern = r"(<!-- BEGIN API ROUTES -->).*?(<!-- END API ROUTES -->)"
    new_readme, count = re.subn(pattern, expected_block, readme_text, flags=re.DOTALL)

    if count == 0:
        print(
            "❌ Could not find <!-- BEGIN API ROUTES --> markers in README.md to replace."
        )
        sys.exit(1)

    README.write_text(new_readme)
    print(f"✅ Updated README.md with {len(routes)} API routes.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or fix API route documentation."
    )
    parser.add_argument(
        "--fix", action="store_true", help="Update README.md with the latest routes."
    )
    args = parser.parse_args()

    routes = get_app_routes_from_openapi()

    if args.fix:
        fix_readme(routes)
        return 0

    if not check_routes_in_readme(routes):
        print("❌ The API routes table in README.md is out of date.\n")
        print("Run `uv run scripts/check_doc_routes.py --fix` to update it.")
        return 1

    print(f"✅ All {len(routes)} API routes are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
