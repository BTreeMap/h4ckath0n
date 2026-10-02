#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py
    uv run scripts/check_doc_routes.py --fix

The script imports the h4ckath0n app, enumerates all routes using OpenAPI schema,
and generates a markdown table. It verifies that this table exactly matches the content
between <!-- START API_ROUTES --> and <!-- END API_ROUTES --> in README.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI paths omitted from user docs.
FRAMEWORK_PATHS = frozenset({"openapi.json", "docs", "docs/oauth2-redirect", "redoc"})


def get_generated_table() -> str:
    """Return the markdown table of all routes from the live FastAPI app."""
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
        if path.lstrip("/") in FRAMEWORK_PATHS:
            continue
        for method, op in path_item.items():
            summary = op.get("summary", "")
            routes.append((method.upper(), path, summary))

    # Sort primarily by path, then method
    routes.sort(key=lambda r: (r[1], r[0]))

    out = ["| Method | Path | Summary |", "|---|---|---|"]
    for method, path, summary in routes:
        out.append(f"| `{method}` | `{path}` | {summary} |")

    return "\n".join(out)


def main() -> int:
    fix = "--fix" in sys.argv
    table = get_generated_table()

    readme_text = README.read_text()

    start_marker = "<!-- START API_ROUTES -->"
    end_marker = "<!-- END API_ROUTES -->"

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(f"❌ Markers {start_marker} and/or {end_marker} not found in README.md.")
        return 1

    current_content = readme_text[start_idx + len(start_marker) : end_idx].strip()

    if current_content != table:
        if fix:
            new_text = (
                readme_text[: start_idx + len(start_marker)]
                + "\n"
                + table
                + "\n"
                + readme_text[end_idx:]
            )
            README.write_text(new_text)
            print("✅ README.md has been updated with the latest API routes.")
            return 0
        else:
            print("❌ API routes in README.md are out of sync with the codebase.")
            print("Run `uv run scripts/check_doc_routes.py --fix` to update.")
            return 1

    print("✅ API routes in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
