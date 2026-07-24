#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that API routes in the FastAPI app are documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--fix]

The script generates a list of API routes from the OpenAPI schema and ensures
it perfectly matches the block between <!-- BEGIN API ROUTES --> and
<!-- END API ROUTES --> in README.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

START_MARKER = "<!-- BEGIN API ROUTES -->"
END_MARKER = "<!-- END API ROUTES -->"


def get_openapi_routes() -> str:
    """Return formatted Markdown string of all API routes."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    openapi = app.openapi()

    lines = []
    for path, path_item in openapi.get("paths", {}).items():
        for method, op in path_item.items():
            if method.lower() not in ("get", "post", "put", "patch", "delete", "options"):
                continue
            summary = op.get("summary", "")
            lines.append(f"- `{method.upper()} {path}` — {summary}")

    return "\n".join(lines) + "\n"


def main() -> int:
    fix = "--fix" in sys.argv

    readme_text = README.read_text()
    start_idx = readme_text.find(START_MARKER)
    end_idx = readme_text.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        print("❌ Markers not found in README.md")
        return 1

    generated = get_openapi_routes()

    prefix = readme_text[: start_idx + len(START_MARKER)] + "\n"
    suffix = readme_text[end_idx:]

    current_block = readme_text[start_idx + len(START_MARKER) : end_idx].lstrip("\n")

    if current_block == generated:
        print("✅ API routes in README.md are up to date.")
        return 0

    if fix:
        README.write_text(prefix + generated + suffix)
        print("🔧 Updated API routes in README.md.")
        return 0

    print("❌ API routes in README.md are out of date.")
    print("Run `uv run scripts/check_doc_routes.py --fix` to update.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
