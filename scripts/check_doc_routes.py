#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script imports the h4ckath0n app, generates a markdown table of routes grouped by tag
from the OpenAPI schema, and ensures that it matches the contents between
<!-- ROUTES_START --> and <!-- ROUTES_END --> in README.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
START_MARKER = "<!-- ROUTES_START -->\n"
END_MARKER = "<!-- ROUTES_END -->\n"


def get_routes_markdown() -> str:
    """Generate markdown table of routes from the live FastAPI app's OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    paths = app.openapi()["paths"]

    groups: dict[str, list[tuple[str, str, str]]] = {}
    for path, methods in paths.items():
        for method, op in methods.items():
            tags: list[str] = op.get("tags", ["default"])
            for tag in tags:
                groups.setdefault(tag, []).append((method.upper(), path, op.get("summary", "")))

    lines: list[str] = []
    for tag in sorted(groups.keys()):
        title = tag.replace("-", " ").title()
        if title == "Default":
            title = "Uncategorized"

        lines.append(f"### {title}")
        lines.append("")
        lines.append("| Method | Path | Summary |")
        lines.append("|---|---|---|")
        for method, path, summary in groups[tag]:
            lines.append(f"| `{method}` | `{path}` | {summary} |")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update README.md in place")
    args = parser.parse_args()

    generated_md = get_routes_markdown()

    readme_text = README.read_text()

    if START_MARKER not in readme_text or END_MARKER not in readme_text:
        print("❌ Could not find ROUTES_START or ROUTES_END markers in README.md", file=sys.stderr)
        return 1

    before_marker, rest = readme_text.split(START_MARKER, 1)
    current_content, after_marker = rest.split(END_MARKER, 1)

    if current_content == generated_md:
        print("✅ API routes in README.md are up to date.")
        return 0

    if args.update:
        new_readme = before_marker + START_MARKER + generated_md + END_MARKER + after_marker
        README.write_text(new_readme)
        print("✅ Updated API routes in README.md.")
        return 0
    else:
        print("❌ API routes in README.md are out of date.", file=sys.stderr)
        print("Run `uv run scripts/check_doc_routes.py --update` to fix.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
