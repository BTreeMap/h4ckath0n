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


def get_app_routes() -> list[tuple[str, str, str]]:
    """Return (method, path, summary) tuples from the live FastAPI app's OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    paths = app.openapi().get("paths", {})
    routes: list[tuple[str, str, str]] = []

    for path, path_item in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, operation in path_item.items():
            method = method.upper()
            if method == "HEAD":
                continue
            summary = operation.get("summary", "")
            routes.append((method, path, summary))

    return sorted(routes, key=lambda x: (x[1], x[0]))


def format_routes_markdown(routes: list[tuple[str, str, str]]) -> str:
    """Format routes as a markdown list."""
    lines = []
    for method, path, summary in routes:
        lines.append(f"- `{method} {path}` — {summary}")
    return "\n".join(lines)


def check_routes_in_readme(
    routes: list[tuple[str, str, str]],
) -> list[tuple[str, str]]:
    """Return routes that are not mentioned anywhere in README.md.

    We look for ``METHOD /path`` (e.g. ``GET /health``) so that sub-path
    matches like ``/auth/passkeys/{key_id}`` inside
    ``/auth/passkeys/{key_id}/revoke`` are not false positives.
    """
    readme_text = README.read_text()
    missing: list[tuple[str, str]] = []
    for method, path, _ in routes:
        # Build a pattern like "GET /health" or "PATCH /auth/passkeys/\{key_id\}"
        # that must appear as a recognisable method+path token in the README.
        path_re = re.escape(path)
        combined = rf"`{method}\s+{path_re}`"
        if not re.search(combined, readme_text, re.IGNORECASE):
            missing.append((method, path))
    return missing


def fix_readme(routes: list[tuple[str, str, str]]) -> bool:
    """Inject the generated routes into README.md between structural markers."""
    readme_text = README.read_text()

    marker_start = "<!-- BEGIN API ROUTES -->"
    marker_end = "<!-- END API ROUTES -->"

    if marker_start not in readme_text or marker_end not in readme_text:
        print("❌ Structural markers not found in README.md.")
        return False

    routes_md = format_routes_markdown(routes)

    pattern = re.compile(
        rf"{re.escape(marker_start)}.*?{re.escape(marker_end)}", re.DOTALL
    )
    new_text = pattern.sub(f"{marker_start}\n{routes_md}\n{marker_end}", readme_text)

    if new_text != readme_text:
        README.write_text(new_text)
        print("✅ README.md updated with latest routes.")
    else:
        print("✅ README.md routes are already up to date.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or fix API route documentation."
    )
    parser.add_argument(
        "--fix", action="store_true", help="Automatically inject routes into README.md"
    )
    args = parser.parse_args()

    routes = get_app_routes()

    if args.fix:
        if not fix_readme(routes):
            return 1
        return 0

    missing = check_routes_in_readme(routes)

    if missing:
        print("❌ The following API routes are NOT documented in README.md:\n")
        for method, path in missing:
            print(f"  {method:6s} {path}")
        print(
            "\nRun `uv run scripts/check_doc_routes.py --fix` to automatically update README.md, "
            "or if intentionally undocumented, add them to FRAMEWORK_PATHS in this script."
        )
        return 1

    print(f"✅ All {len(routes)} API routes are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
