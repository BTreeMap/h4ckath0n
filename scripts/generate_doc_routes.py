#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/generate_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes, and checks that
README.md mentions each one. Routes provided by FastAPI itself (e.g. /openapi.json,
/docs, /redoc) are excluded from the check.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI paths omitted from user docs.
FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


def get_openapi_routes() -> str:
    """Generate the markdown for API routes using the live FastAPI app."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    paths = app.openapi().get("paths", {})
    routes_by_tag = defaultdict(list)

    # Track all seen tags to ensure we don't miss any new ones
    seen_tags = set()
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            tags = op.get("tags", [])
            tag = tags[0] if tags else "default"
            seen_tags.add(tag)
            summary = op.get("summary", "")
            routes_by_tag[tag].append(f"- `{method.upper()} {path}` — {summary}")

    # Defined order for known tags, any new tags will be appended at the end
    tag_order = [
        "default",
        "auth",
        "passkey",
        "password-auth",
        "jobs",
        "uploads",
        "llm",
    ]
    for tag in sorted(seen_tags):
        if tag not in tag_order:
            tag_order.append(tag)

    lines = []
    for tag in tag_order:
        if tag in routes_by_tag:
            if tag != "default":
                lines.append(f"### {tag.replace('-', ' ').title()}")
            for r in routes_by_tag[tag]:
                lines.append(r)
            lines.append("")
    return "\n".join(lines).strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check or update generated API routes in README."
    )
    parser.add_argument(
        "--update", action="store_true", help="Update README.md in place."
    )
    args = parser.parse_args()

    generated = get_openapi_routes()
    readme_text = README.read_text()

    marker_begin = "<!-- BEGIN ROUTES -->"
    marker_end = "<!-- END ROUTES -->"

    pattern = re.compile(rf"{marker_begin}.*?{marker_end}", re.DOTALL)
    if not pattern.search(readme_text):
        print(f"❌ Error: {marker_begin} and {marker_end} not found in README.md")
        return 1

    new_section = f"{marker_begin}\n\n{generated}\n\n{marker_end}"
    new_readme_text = pattern.sub(new_section, readme_text)

    if new_readme_text == readme_text:
        print("✅ README.md API routes are up-to-date.")
        return 0

    if args.update:
        README.write_text(new_readme_text)
        print("✅ README.md updated successfully.")
        return 0
    else:
        print("❌ README.md API routes are out of date. Run with --update to fix.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
