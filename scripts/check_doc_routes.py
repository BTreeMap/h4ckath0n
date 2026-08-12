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
FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


def get_app_routes() -> tuple[list[tuple[str, str]], dict[str, dict[str, str]]]:
    """Return (method, path) pairs and route details from the live FastAPI app."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    paths = app.openapi().get("paths", {})

    routes: list[tuple[str, str]] = []
    details: dict[str, dict[str, str]] = {}
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            method_upper = method.upper()
            routes.append((method_upper, path))
            details[f"{method_upper} {path}"] = {
                "summary": op.get("summary", ""),
                "description": op.get("description", ""),
            }
    return sorted(routes), details


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


def fix_readme(
    routes: list[tuple[str, str]], details: dict[str, dict[str, str]]
) -> None:
    """Generate and inject the API routes list into README.md."""
    readme_text = README.read_text()

    lines = []
    for method, path in routes:
        info = details.get(f"{method} {path}", {})
        summary = info.get("summary", "")
        if summary:
            lines.append(f"- `{method} {path}` — {summary.lower()}")
        else:
            lines.append(f"- `{method} {path}`")

    generated = "\n".join(lines)

    pattern = r"(<!-- BEGIN API ROUTES -->\n).*?(<!-- END API ROUTES -->)"
    replacement = rf"\1{generated}\n\2"

    new_text = re.sub(pattern, replacement, readme_text, flags=re.DOTALL)
    README.write_text(new_text)
    print("✅ Regenerated API routes in README.md.")


def main() -> int:
    routes, details = get_app_routes()

    if "--fix" in sys.argv:
        fix_readme(routes, details)
        return 0

    missing = check_routes_in_readme(routes)

    if missing:
        print("❌ The following API routes are NOT documented in README.md:\n")
        for method, path in missing:
            print(f"  {method:6s} {path}")
        print("\nAdd these routes to README.md or run this script with --fix.")
        return 1

    print(f"✅ All {len(routes)} API routes are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
