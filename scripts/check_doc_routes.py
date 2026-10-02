#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, dynamically retrieves OpenAPI endpoints,
generates the Markdown documentation representation for them, and checks that
the exact content is present between <!-- BEGIN ROUTES --> and <!-- END ROUTES -->
in the README.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def format_tag_header(tag: str) -> str | None:
    if tag == "default":
        return None
    if tag == "auth":
        return "### Session"
    if tag == "passkey":
        return "### Passkeys"
    if tag == "password-auth":
        return "### Password Auth"
    if tag == "jobs":
        return "### Background Jobs"
    if tag == "uploads":
        return "### Uploads"
    if tag == "llm":
        return "### LLM Chat"
    return f"### {tag.title()}"


def get_generated_routes() -> str:
    """Return the formatted Markdown content for API routes."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    app = create_app(
        Settings(database_url="sqlite+aiosqlite://", password_auth_enabled=True)
    )
    paths = app.openapi().get("paths", {})

    routes_by_tag: dict[str, list[tuple[str, str, str]]] = {}
    for path, item in paths.items():
        for method, op in item.items():
            if method.lower() == "head":
                continue
            tags = op.get("tags", ["default"])
            for tag in tags:
                if tag not in routes_by_tag:
                    routes_by_tag[tag] = []
                route_info = (method.upper(), path, op.get("summary", ""))
                if route_info not in routes_by_tag[tag]:
                    routes_by_tag[tag].append(route_info)

    tag_order = [
        "default",
        "auth",
        "passkey",
        "password-auth",
        "jobs",
        "uploads",
        "llm",
    ]
    sorted_tags = sorted(
        routes_by_tag.keys(),
        key=lambda t: tag_order.index(t) if t in tag_order else 999,
    )

    lines = []
    for tag in sorted_tags:
        header = format_tag_header(tag)
        if header:
            lines.append(header)
        for method, path, summary in routes_by_tag[tag]:
            lines.append(f"- `{method} {path}` — {summary.lower()}")
        lines.append("")

    return "\n".join(lines).strip()


def main() -> int:
    readme_text = README.read_text()
    generated = get_generated_routes()

    # Extract content between markers
    match = re.search(
        r"<!-- BEGIN ROUTES -->\n(.*?)\n<!-- END ROUTES -->", readme_text, re.DOTALL
    )

    if not match:
        print("❌ Error: <!-- BEGIN ROUTES --> ... not found in README.md.")
        return 1

    existing_content = match.group(1).strip()

    if existing_content != generated:
        print("❌ Error: API routes in README.md are out of date.")
        print("\nExpected content between markers:\n")
        print(generated)
        print("\nPlease run a script to update them, or copy the above into README.md.")
        return 1

    print("✅ API routes in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
