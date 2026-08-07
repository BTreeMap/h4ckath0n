#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--fix]
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI internal paths that we do not require in user docs.
FRAMEWORK_PATHS = frozenset({"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"})


def generate_routes_markdown() -> str:
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(database_url="sqlite+aiosqlite://", password_auth_enabled=True)
    app = create_app(settings)
    openapi = app.openapi()

    routes_by_tag = {}
    for path, methods in openapi.get("paths", {}).items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, details in methods.items():
            tag = details.get("tags", ["General"])[0]
            if tag not in routes_by_tag:
                routes_by_tag[tag] = []
            routes_by_tag[tag].append((method.upper(), path, details.get("summary", "")))

    lines = []
    for tag in sorted(routes_by_tag.keys()):
        lines.append(f"### {tag}")
        for method, path, summary in sorted(routes_by_tag[tag], key=lambda x: x[1]):
            lines.append(f"- `` `{method} {path}` `` — {summary.lower()}")
        lines.append("")
    return "\n".join(lines).strip()


def main() -> int:
    expected_markdown = generate_routes_markdown()

    readme_text = README.read_text()

    start_marker = "<!-- BEGIN API ROUTES -->"
    end_marker = "<!-- END API ROUTES -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Markers not found in README.md")
        return 1

    start_idx = readme_text.find(start_marker) + len(start_marker)
    end_idx = readme_text.find(end_marker)

    current_markdown = readme_text[start_idx:end_idx].strip()

    if current_markdown != expected_markdown:
        if "--fix" in sys.argv:
            new_readme = (
                readme_text[:start_idx]
                + "\n\n"
                + expected_markdown
                + "\n\n"
                + readme_text[end_idx:]
            )
            README.write_text(new_readme)
            print("✅ Updated README.md with generated routes.")
            return 0
        else:
            print("❌ README.md routes do not match generated routes. Run with --fix to update.")
            return 1

    print("✅ API routes in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
