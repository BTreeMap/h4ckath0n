#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the API routes in README.md perfectly match the app.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script generates the exact markdown block of routes from the OpenAPI schema.
It enforces that the content between <!-- BEGIN API ROUTES --> and <!-- END API ROUTES -->
is exactly this generated block. Use --update to automatically apply fixes.
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


def get_generated_markdown() -> str:
    """Generate the full markdown block for all documented API routes."""
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    # Retrieve routes using the OpenAPI schema for reliable enumeration.
    paths = app.openapi().get("paths", {})
    routes: list[tuple[str, str, str]] = []

    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, details in methods.items():
            summary = details.get("summary", "")
            routes.append((method.upper(), path, summary))

    # Sort logically by path then method
    routes.sort(key=lambda x: (x[1], x[0]))

    lines = ["<!-- BEGIN API ROUTES -->"]
    for method, path, summary in routes:
        if summary:
            lines.append(f"- `{method} {path}` — {summary}")
        else:
            lines.append(f"- `{method} {path}`")
    lines.append("<!-- END API ROUTES -->")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update the README in place")
    args = parser.parse_args()

    readme_text = README.read_text()
    generated_block = get_generated_markdown()

    begin_marker = "<!-- BEGIN API ROUTES -->"
    end_marker = "<!-- END API ROUTES -->"

    start_idx = readme_text.find(begin_marker)
    end_idx = readme_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(f"❌ Missing markers '{begin_marker}' and '{end_marker}' in README.md")
        return 1

    # Extract existing block including markers
    existing_block = readme_text[start_idx : end_idx + len(end_marker)]

    if existing_block == generated_block:
        print("✅ API routes in README.md match the live application.")
        return 0

    if args.update:
        new_readme_text = (
            readme_text[:start_idx] + generated_block + readme_text[end_idx + len(end_marker) :]
        )
        README.write_text(new_readme_text)
        print("✅ README.md updated successfully with actual API routes.")
        return 0
    else:
        print("❌ API routes in README.md are outdated.")
        print("\nExpected block:\n")
        print(generated_block)
        print("\nRun `uv run scripts/check_doc_routes.py --update` to fix.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
