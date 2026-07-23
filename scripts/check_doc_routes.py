#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the API routes in README.md exactly match the app's OpenAPI schema.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, generates a markdown section of all routes,
and checks that it matches the content between <!-- routes-start --> and <!-- routes-end --> in README.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI internal paths that we do not require in user docs.
FRAMEWORK_PATHS = frozenset({"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"})

TAG_TITLES = {
    "System": "System",
    "passkey": "Passkeys (Default Auth)",
    "auth": "Session",
    "jobs": "Background Jobs",
    "uploads": "Uploads",
    "llm": "LLM Chat",
    "password-auth": "Password Auth (Optional)",
}

def generate_routes_markdown() -> str:
    """Generate the markdown table of routes from the OpenAPI schema."""
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    paths = app.openapi().get("paths", {})

    routes_by_tag: dict[str, list[tuple[str, str, str]]] = {}
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            if method.lower() == "head":
                continue
            tags = op.get("tags", [])
            tag = tags[0] if tags else "System"
            summary = op.get("summary", "")
            if tag not in routes_by_tag:
                routes_by_tag[tag] = []
            routes_by_tag[tag].append((method.upper(), path, summary))

    lines = []
    lines.append("<!-- routes-start -->")

    order = ["System", "passkey", "password-auth", "auth", "jobs", "uploads", "llm"]
    sorted_tags = sorted(routes_by_tag.keys(), key=lambda t: order.index(t) if t in order else len(order))

    for tag in sorted_tags:
        title = TAG_TITLES.get(tag, tag.capitalize())
        lines.append(f"### {title}")
        lines.append("")
        lines.append("| Method | Path | Summary |")
        lines.append("|---|---|---|")
        for method, path, summary in sorted(routes_by_tag[tag], key=lambda x: (x[1], x[0])):
            lines.append(f"| `{method}` | `{path}` | {summary} |")
        lines.append("")

    lines.append("<!-- routes-end -->")
    return "\n".join(lines)


def main() -> int:
    readme_text = README.read_text()
    start_marker = "<!-- routes-start -->"
    end_marker = "<!-- routes-end -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Could not find <!-- routes-start --> or <!-- routes-end --> markers in README.md.")
        return 1

    expected_md = generate_routes_markdown()

    start_idx = readme_text.index(start_marker)
    end_idx = readme_text.index(end_marker) + len(end_marker)
    actual_md = readme_text[start_idx:end_idx]

    if actual_md != expected_md:
        print("❌ The API routes in README.md are out of date or incorrectly formatted.")
        print("Expected block:\n")
        print(expected_md)
        print("\n\nPlease update README.md to match exactly, or update scripts/check_doc_routes.py.")
        return 1

    print("✅ All API routes in README.md are correctly documented and up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
