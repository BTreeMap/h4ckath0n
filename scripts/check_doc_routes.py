#!/usr/bin/env -S uv run python
"""Drift-prevention check: generate and verify API route documentation.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes from the OpenAPI schema,
groups them by tags, and generates a markdown section.
It then checks if README.md contains the exact generated section between
<!-- ROUTES:START --> and <!-- ROUTES:END -->. If not, it updates README.md.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

FRAMEWORK_PATHS = frozenset({"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"})


def generate_routes_markdown() -> str:
    """Generate the markdown for API routes grouped by tags."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    schema = app.openapi()

    routes_by_tag: dict[str, list[tuple[str, str, str]]] = {}
    for path, path_item in schema.get("paths", {}).items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in path_item.items():
            tags = op.get("tags", ["Default"])
            tag = tags[0]
            routes_by_tag.setdefault(tag, []).append((method.upper(), path, op.get("summary", "")))

    lines = []
    for tag in sorted(routes_by_tag.keys()):
        lines.append(f"### {tag.replace('-', ' ').title()}")
        for method, path, summary in routes_by_tag[tag]:
            lines.append(f"- `{method} {path}` — {summary}")
        lines.append("")

    # Remove the very last empty line to avoid extra trailing newline
    if lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


def main() -> int:
    readme_text = README.read_text()

    start_marker = "<!-- ROUTES:START -->"
    end_marker = "<!-- ROUTES:END -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("❌ Could not find ROUTES:START or ROUTES:END markers in README.md.")
        return 1

    generated = generate_routes_markdown()

    pattern = re.compile(f"{re.escape(start_marker)}.*{re.escape(end_marker)}", re.DOTALL)

    replacement = f"{start_marker}\n{generated}\n{end_marker}"

    new_readme_text = pattern.sub(replacement, readme_text)

    if new_readme_text == readme_text:
        print("✅ API routes in README.md are up to date.")
        return 0

    print("⚠️ API routes in README.md were out of date. Updating...")
    README.write_text(new_readme_text)
    print("✅ Updated README.md.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
