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


def get_app_routes() -> list[tuple[str, str, str]]:
    """Return (method, path, summary) tuples from the live FastAPI app OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    schema = app.openapi()
    paths = schema.get("paths", {})

    routes = []
    for path, operations in paths.items():
        for method, op in operations.items():
            routes.append((method.upper(), path, op.get("summary", "")))

    return sorted(routes, key=lambda x: (x[1], x[0]))


def generate_routes_section(routes: list[tuple[str, str, str]]) -> str:
    """Generate the markdown section for routes."""
    lines = ["<!-- BEGIN API ROUTES -->"]
    for method, path, summary in routes:
        lines.append(f"- `{method} {path}` — {summary}")
    lines.append("<!-- END API ROUTES -->")
    return "\n".join(lines)


def update_readme(new_section: str) -> bool:
    """Update README.md with the new routes section. Returns True if changed."""
    readme_text = README.read_text()
    pattern = r"<!-- BEGIN API ROUTES -->.*?<!-- END API ROUTES -->"

    match = re.search(pattern, readme_text, flags=re.DOTALL)
    if not match:
        print("❌ Could not find <!-- BEGIN API ROUTES --> markers in README.md.")
        sys.exit(1)

    old_section = match.group(0)
    if old_section == new_section:
        return False

    updated_text = (
        readme_text[: match.start()] + new_section + readme_text[match.end() :]
    )
    README.write_text(updated_text)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or fix documented API routes.")
    parser.add_argument(
        "--fix", action="store_true", help="Update README.md automatically."
    )
    args = parser.parse_args()

    routes = get_app_routes()
    new_section = generate_routes_section(routes)

    if args.fix:
        changed = update_readme(new_section)
        if changed:
            print(f"✅ Updated README.md with {len(routes)} API routes.")
        else:
            print(f"✅ README.md is already up to date with {len(routes)} API routes.")
        return 0
    else:
        readme_text = README.read_text()
        pattern = r"<!-- BEGIN API ROUTES -->.*?<!-- END API ROUTES -->"
        match = re.search(pattern, readme_text, flags=re.DOTALL)
        if not match:
            print("❌ Could not find <!-- BEGIN API ROUTES --> markers in README.md.")
            return 1

        old_section = match.group(0)
        if old_section != new_section:
            print(
                "❌ API routes in README.md are out of date. Run with --fix to update."
            )
            return 1

        print(f"✅ All {len(routes)} API routes are documented correctly in README.md.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
