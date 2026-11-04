#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that API routes in README.md exactly match the live app.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, gets the OpenAPI schema, and generates a markdown
list of routes grouped by tag. It then ensures that README.md contains this exact output
between <!-- BEGIN ROUTES --> and <!-- END ROUTES -->.
"""

from __future__ import annotations

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


def get_generated_routes_markdown() -> str:
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    paths = app.openapi().get("paths", {})

    routes_by_tag: dict[str, list[str]] = defaultdict(list)
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            tags = op.get("tags", ["default"])
            tag = tags[0] if tags else "default"
            summary = op.get("summary", "")
            routes_by_tag[tag].append(f"- `{method.upper()} {path}` - {summary}")

    lines = []
    for tag in sorted(routes_by_tag.keys()):
        lines.append(f"### {tag}")
        for route_str in routes_by_tag[tag]:
            lines.append(route_str)
        lines.append("")

    return "\n".join(lines).strip()


def main() -> int:
    expected_markdown = get_generated_routes_markdown()

    readme_text = README.read_text()

    match = re.search(
        r"<!-- BEGIN ROUTES -->\n(.*?)\n<!-- END ROUTES -->", readme_text, re.DOTALL
    )
    if not match:
        print(
            "❌ Could not find <!-- BEGIN ROUTES --> and <!-- END ROUTES --> markers in README.md."
        )
        return 1

    actual_markdown = match.group(1).strip()

    if actual_markdown != expected_markdown:
        print("❌ API routes in README.md do not match the live application.")
        print("\nExpected block between markers:\n")
        print(expected_markdown)
        print("\nPlease update README.md.")
        return 1

    print("✅ API routes in README.md are up to date and match the application.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
