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


def get_app_routes() -> list[tuple[str, str, str, str]]:
    """Return (method, path, summary, description) tuples from the live FastAPI app."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    openapi = app.openapi()
    routes: list[tuple[str, str, str, str]] = []

    for path, methods in openapi["paths"].items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            routes.append(
                (
                    method.upper(),
                    path,
                    op.get("summary", ""),
                    op.get("description", ""),
                )
            )

    # Sort by path, then method
    routes.sort(key=lambda x: (x[1], x[0]))
    return routes


def generate_routes_markdown(routes: list[tuple[str, str, str, str]]) -> str:
    """Generate a markdown table of routes."""
    lines = [
        "| Method | Path | Summary | Description |",
        "|---|---|---|---|",
    ]
    for method, path, summary, description in routes:
        # Clean up description (remove newlines to keep it in one table row)
        desc_clean = description.replace("\n", " ").strip()
        lines.append(f"| `{method}` | `{path}` | {summary} | {desc_clean} |")
    return "\n".join(lines)


def update_readme_routes(routes_md: str) -> None:
    """Update README.md between the API routes markers."""
    readme_text = README.read_text()

    pattern = re.compile(r"(<!-- BEGIN_API_ROUTES -->).*?(<!-- END_API_ROUTES -->)", re.DOTALL)

    if not pattern.search(readme_text):
        print(
            "❌ Could not find <!-- BEGIN_API_ROUTES --> and "
            "<!-- END_API_ROUTES --> markers in README.md."
        )
        sys.exit(1)

    new_text = pattern.sub(lambda m: f"{m.group(1)}\n{routes_md}\n{m.group(2)}", readme_text)
    README.write_text(new_text)


def check_routes_in_readme(routes_md: str) -> bool:
    """Check if the exact generated markdown block exists in the README."""
    readme_text = README.read_text()

    pattern = re.compile(r"<!-- BEGIN_API_ROUTES -->\n(.*?)\n<!-- END_API_ROUTES -->", re.DOTALL)
    match = pattern.search(readme_text)

    if not match:
        print("❌ Could not find API route markers in README.md.")
        return False

    current_md = match.group(1).strip()
    expected_md = routes_md.strip()

    return current_md == expected_md


def main() -> int:
    fix_mode = "--fix" in sys.argv
    routes = get_app_routes()
    routes_md = generate_routes_markdown(routes)

    if fix_mode:
        update_readme_routes(routes_md)
        print(f"✅ Generated {len(routes)} API routes in README.md.")
        return 0

    if not check_routes_in_readme(routes_md):
        print("❌ API routes in README.md are outdated or missing.")
        print("Run `uv run scripts/check_doc_routes.py --fix` to update them.")
        return 1

    print(f"✅ All {len(routes)} API routes are documented accurately in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
