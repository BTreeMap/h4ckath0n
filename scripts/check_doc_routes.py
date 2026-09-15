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

# FastAPI paths omitted from user docs.
FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


BEGIN_MARKER = "<!-- BEGIN ROUTES -->"
END_MARKER = "<!-- END ROUTES -->"


def generate_routes_markdown() -> str:
    """Return generated markdown list of routes from the live FastAPI app."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    routes: list[str] = []
    paths = app.openapi().get("paths", {})
    for path, methods_dict in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods_dict.items():
            if method.upper() == "HEAD":
                continue
            summary = op.get("summary", "")
            routes.append(f"- `{method.upper()} {path}` — {summary}")

    return "\n".join(sorted(routes))


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update README.md inline")
    args = parser.parse_args()

    generated_md = generate_routes_markdown()
    readme_text = README.read_text()

    pattern = re.compile(rf"{BEGIN_MARKER}\n.*?{END_MARKER}", re.DOTALL)
    if not pattern.search(readme_text):
        print(f"❌ Markers {BEGIN_MARKER} and {END_MARKER} not found in README.md")
        return 1

    expected_readme = pattern.sub(
        f"{BEGIN_MARKER}\n{generated_md}\n{END_MARKER}", readme_text
    )

    if readme_text != expected_readme:
        if args.update:
            README.write_text(expected_readme)
            print("✅ README.md updated with latest routes.")
            return 0
        else:
            print(
                "❌ API routes in README.md are out of sync. Run with --update to fix."
            )
            return 1

    print("✅ API routes in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
